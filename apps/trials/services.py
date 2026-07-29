"""
Immortal Trial state transitions — the only place application state mutates.

Each verb performs the authoritative DB change (status, timestamps, timeline
comment) and — in the SAME transaction — enqueues the Discord side-effect onto
the `trial_sync_queue` outbox for the host daemon to replay (transactional
outbox: the intent commits atomically with the state change). Internal staff
comments never enqueue: the daemon posts to a channel applicants may read.

Acceptance performs the site's first write to a game-owned `accounts` column:
a guarded single-column UPDATE granting `immortal_level = IMMORTAL`, never a
downgrade and never a full-row save.
"""
import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone

from apps.accounts.models import Account, ImmortalLevel
from apps.core.utils.staff import staff_name  # noqa: F401 - shared, re-exported
from apps.core.utils.text import clean_text

from . import eligibility
from .models import (
    OPEN_STATUSES,
    REVIEW_WINDOW,
    TrialApplication,
    TrialComment,
    TrialCommentKind,
    TrialStatus,
    TrialSyncAction,
    TrialSyncTask,
    TrialTrack,
)

log = logging.getLogger(__name__)

CHARACTER_MAX = 64
PROPOSAL_MAX = 4000
EXPERIENCE_MAX = 4000
COMMENT_MAX = 2000
REASON_MAX = 255


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _now():
    return timezone.now()


def _add_comment(application, kind, author, body, is_internal=False) -> TrialComment:
    return TrialComment.objects.create(
        application=application,
        kind=kind,
        is_internal=is_internal,
        author=author,
        body=body,
        created_at=_now(),
    )


def add_system_comment(application, actor, body) -> TrialComment:
    """Record a state change on the timeline (the audit trail)."""
    return _add_comment(application, TrialCommentKind.SYSTEM, actor, body)


def enqueue(application, action, actor, payload=None) -> None:
    """Append a Discord side-effect intent to the outbox, inside the action's
    transaction, so delivery intent commits atomically with the state change."""
    TrialSyncTask.objects.create(
        application=application,
        action=action,
        actor=actor,
        payload=payload or {},
        created_at=_now(),
    )


def _validate_fields(data) -> dict:
    """Validate and sanitize the application form fields (submit + resubmit)."""
    character_name = clean_text(data.get("character_name"), CHARACTER_MAX)
    track = data.get("track")
    proposal = clean_text(data.get("proposal"), PROPOSAL_MAX)
    experience = clean_text(data.get("experience"), EXPERIENCE_MAX)
    if not character_name:
        raise ValidationError("Which character are you known by?")
    if track not in TrialTrack:
        raise ValidationError("Pick a track: Zoner or Coder.")
    if not proposal:
        raise ValidationError("A project proposal is required.")
    if not data.get("ack_ai_policy"):
        raise ValidationError(
            "You must acknowledge the original-work policy for trial writing."
        )
    if not data.get("ack_commitment"):
        raise ValidationError(
            "You must acknowledge the time and communication commitment."
        )
    return {
        "character_name": character_name,
        "track": track,
        "proposal": proposal,
        "experience": experience,
        "ack_ai_policy": True,
        "ack_commitment": True,
    }


def _applicant_name(account) -> str:
    """Attribution for applicant-authored timeline entries."""
    application = account.trial_applications.order_by("-id").first()
    if application and application.character_name:
        return application.character_name
    return account.get_username()


# --------------------------------------------------------------------------- #
# Applicant actions
# --------------------------------------------------------------------------- #

def submit(account, data) -> TrialApplication:
    """Create a new application and start the 7-day review clock."""
    fields = _validate_fields(data)
    if TrialApplication.objects.filter(
        account=account, status__in=OPEN_STATUSES
    ).exists():
        raise ValidationError("You already have an open application.")
    now = _now()
    try:
        with transaction.atomic():
            application = TrialApplication.objects.create(
                account=account,
                status=TrialStatus.SUBMITTED,
                open_slot=account.account_id,
                submitted_at=now,
                due_at=now + REVIEW_WINDOW,
                **fields,
            )
            add_system_comment(
                application, fields["character_name"], "Application submitted."
            )
            payload = {
                "track": fields["track"],
                "character_name": fields["character_name"],
                **eligibility.check(account).as_payload(),
            }
            enqueue(
                application,
                TrialSyncAction.SUBMITTED,
                fields["character_name"],
                payload,
            )
    except IntegrityError:
        # The open_slot unique constraint caught a double-submit race.
        raise ValidationError("You already have an open application.")
    return application


def resubmit(application, account, data) -> TrialApplication:
    """Revise a sent-back application; restarts the 7-day review clock."""
    if application.account_id != account.account_id:
        raise ValidationError("This is not your application.")
    if application.status != TrialStatus.NEEDS_REVISION:
        raise ValidationError("This application is not awaiting revision.")
    fields = _validate_fields(data)
    now = _now()
    with transaction.atomic():
        for name, value in fields.items():
            setattr(application, name, value)
        application.status = TrialStatus.SUBMITTED
        application.submitted_at = now
        application.due_at = now + REVIEW_WINDOW
        application.revision_count += 1
        application.save(update_fields=(
            *fields, "status", "submitted_at", "due_at", "revision_count",
        ))
        add_system_comment(
            application, fields["character_name"], "Revised and resubmitted."
        )
        payload = {
            "track": fields["track"],
            "character_name": fields["character_name"],
            **eligibility.check(account).as_payload(),
        }
        enqueue(
            application,
            TrialSyncAction.RESUBMITTED,
            fields["character_name"],
            payload,
        )
    return application


def applicant_reply(application, account, text) -> str:
    """Applicant posts to the thread while the application is open."""
    if application.account_id != account.account_id:
        raise ValidationError("This is not your application.")
    if not application.is_open():
        raise ValidationError("This application is closed.")
    text = clean_text(text, COMMENT_MAX)
    if not text:
        raise ValidationError("A reply cannot be empty.")
    author = _applicant_name(account)
    with transaction.atomic():
        _add_comment(application, TrialCommentKind.APPLICANT, author, text)
        enqueue(application, TrialSyncAction.REPLY, author, {"text": text})
    return "Reply posted."


def withdraw(application, account) -> str:
    """Applicant withdraws an open application, freeing the open slot."""
    if application.account_id != account.account_id:
        raise ValidationError("This is not your application.")
    if not application.is_open():
        raise ValidationError("This application is already closed.")
    author = _applicant_name(account)
    with transaction.atomic():
        application.status = TrialStatus.WITHDRAWN
        application.open_slot = None
        application.decided_at = _now()
        application.save(update_fields=("status", "open_slot", "decided_at"))
        add_system_comment(application, author, "Application withdrawn.")
        enqueue(application, TrialSyncAction.WITHDRAWN, author)
    return "Application withdrawn."


# --------------------------------------------------------------------------- #
# Staff actions
# --------------------------------------------------------------------------- #

def staff_comment(application, actor, text, internal=False) -> str:
    """Staff comment — applicant-facing by default, or internal-only."""
    text = clean_text(text, COMMENT_MAX)
    if not text:
        raise ValidationError("A comment cannot be empty.")
    with transaction.atomic():
        _add_comment(
            application, TrialCommentKind.STAFF, actor, text, is_internal=internal
        )
        # Internal notes never reach the outbox: the daemon posts to Discord,
        # where the applicant may be reading.
        if not internal:
            enqueue(application, TrialSyncAction.COMMENT, actor, {"text": text})
    kind = "Internal note" if internal else "Comment"
    return f"{kind} added to application #{application.pk}."


def send_back(application, actor, note) -> str:
    """Send back for revision — unlocks the form for the applicant."""
    note = clean_text(note, COMMENT_MAX)
    if not note:
        raise ValidationError(
            "A revision request needs a note telling the applicant what to fix."
        )
    if application.status == TrialStatus.NEEDS_REVISION:
        return f"Application #{application.pk} is already awaiting revision."
    if not application.is_open():
        raise ValidationError("This application has already been decided.")
    with transaction.atomic():
        application.status = TrialStatus.NEEDS_REVISION
        application.save(update_fields=("status",))
        add_system_comment(application, actor, f"Needs revision: {note}")
        enqueue(application, TrialSyncAction.NEEDS_REVISION, actor, {"note": note})
    return f"Application #{application.pk} sent back for revision."


def reject(application, actor, reason) -> str:
    """Reject with a required reason (shown to the applicant)."""
    reason = clean_text(reason, REASON_MAX)
    if not reason:
        raise ValidationError("A rejection requires a reason.")
    if not application.is_open():
        raise ValidationError("This application has already been decided.")
    with transaction.atomic():
        application.status = TrialStatus.REJECTED
        application.rejection_reason = reason
        application.decided_by = actor
        application.decided_at = _now()
        application.open_slot = None
        application.save(update_fields=(
            "status", "rejection_reason", "decided_by", "decided_at", "open_slot",
        ))
        add_system_comment(application, actor, f"Rejected: {reason}")
        enqueue(application, TrialSyncAction.REJECTED, actor, {"reason": reason})
    return f"Application #{application.pk} rejected."


def accept(application, actor) -> str:
    """Accept — and grant Immortal (Trial) rank if the account has none."""
    if not application.is_open():
        raise ValidationError("This application has already been decided.")
    with transaction.atomic():
        application.status = TrialStatus.ACCEPTED
        application.decided_by = actor
        application.decided_at = _now()
        application.open_slot = None
        application.save(update_fields=(
            "status", "decided_by", "decided_at", "open_slot",
        ))
        # First site-side write to a game-owned accounts column (the table is
        # managed = False). Guarded single-column queryset UPDATE only — never
        # account.save(), which would rewrite every game-owned field — and
        # never a downgrade: 0/None -> IMMORTAL only. An account already
        # holding a rank is accepted without touching the column.
        granted = bool(Account.objects.filter(
            Q(immortal_level__isnull=True) | Q(immortal_level=ImmortalLevel.NONE),
            pk=application.account_id,
        ).update(immortal_level=ImmortalLevel.IMMORTAL))
        add_system_comment(application, actor, "Accepted — welcome to the trial.")
        if granted:
            add_system_comment(application, actor, "Granted Immortal (Trial) rank.")
        enqueue(application, TrialSyncAction.ACCEPTED, actor, {"granted": granted})
    return f"Application #{application.pk} accepted."
