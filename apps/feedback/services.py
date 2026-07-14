"""
Staff feedback actions — the website counterpart to the in-game `reports`
command (ishar-mud `rust-interop/src/feedback.rs`).

Each function performs the authoritative **DB** change (state, resolution,
timestamps, timeline comment) exactly as the Rust `set_state_internal` /
`rust_feedback_*` functions do, and — in the SAME transaction — enqueues the
networked **side-effects** (Discord echo, GitHub sync / issue / `@claude`) onto
the `feedback_sync_queue` outbox for the host daemon to replay. This is a
transactional outbox: the intent commits atomically with the state change, so a
side-effect is never silently lost. The queue table is a hard dependency — apply
the game migration `2026-07-10-000000-0000_feedback_sync_queue` before deploying
(the daemon *process* may lag; rows simply accumulate as `pending`).

The state-machine semantics here must stay in lock-step with `feedback.rs`; the
inline comments cite the Rust behaviour they mirror.
"""
import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.core.utils.staff import staff_name  # noqa: F401 - shared, re-exported

from .models import (
    CommentSource,
    Feedback,
    FeedbackComment,
    FeedbackResolution,
    FeedbackState,
    FeedbackSyncTask,
    SyncAction,
)

log = logging.getLogger(__name__)

# Match the caps enforced in feedback.rs (BODY_MAX_CHARS / note / instructions).
COMMENT_MAX = 2000
NOTE_MAX = 255
INSTRUCTIONS_MAX = 2000


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

# Bidirectional/direction-override codepoints that can spoof displayed order —
# stripped to match the Rust `sanitize_text` (feedback.rs).
_BIDI_OVERRIDES = frozenset(
    chr(cp) for cp in list(range(0x202A, 0x202F)) + list(range(0x2066, 0x206A))
)


def _clean(text, limit) -> str:
    """Strip control + bidi-override characters and truncate — mirrors
    `sanitize_text`."""
    if not text:
        return ""
    cleaned = "".join(
        ch for ch in str(text)
        if (ch in ("\n", "\t") or ord(ch) >= 0x20) and ch not in _BIDI_OVERRIDES
    ).strip()
    if len(cleaned) > limit:
        cleaned = cleaned[:limit].rstrip()
    return cleaned


def _now():
    return timezone.now()


def _add_comment(feedback, source, author, body, is_staff) -> FeedbackComment:
    """Insert a timeline comment. `created_at` is set explicitly because the
    game table is NOT NULL DEFAULT CURRENT_TIMESTAMP and Django would otherwise
    send NULL."""
    return FeedbackComment.objects.create(
        feedback=feedback,
        source=source,
        author=author,
        is_staff=is_staff,
        body=body,
        created_at=_now(),
    )


def add_system_comment(feedback, actor, body) -> FeedbackComment:
    """Record a staff action on the timeline (mirrors `add_system_comment`)."""
    return _add_comment(feedback, CommentSource.SYSTEM, actor, body, is_staff=True)


def _ack_if_needed(feedback, actor) -> bool:
    """
    Claim the report for `actor` if still unclaimed (single-ack model, mirrors
    `ack_if_needed`). Returns True if this call performed the acknowledgement.
    Uses a guarded UPDATE so a concurrent claim can't be overwritten.
    """
    updated = Feedback.objects.filter(
        pk=feedback.pk, acknowledged_by__isnull=True
    ).update(acknowledged_by=actor, acknowledged_at=_now())
    if updated:
        feedback.acknowledged_by = actor
        feedback.acknowledged_at = _now()
        return True
    return False


def enqueue(feedback, action, actor, payload=None) -> None:
    """
    Append a side-effect intent to the outbox. Call inside the action's
    transaction so the intent commits atomically with the state change
    (transactional outbox): guaranteed delivery, no lost side-effects. Any DB
    error propagates and rolls the whole action back, rather than committing a
    state change whose side-effects silently vanished.
    """
    FeedbackSyncTask.objects.create(
        feedback=feedback,
        action=action,
        actor=actor,
        payload=payload or {},
        created_at=_now(),
    )


# --------------------------------------------------------------------------- #
# Actions — each mirrors a `reports` subcommand
# --------------------------------------------------------------------------- #

def acknowledge(feedback, actor) -> str:
    """`reports ack` — claim the report (single-ack)."""
    with transaction.atomic():
        claimed = _ack_if_needed(feedback, actor)
        if not claimed:
            return f"Report #{feedback.pk} already acknowledged by {feedback.acknowledged_by}."
        add_system_comment(feedback, actor, "Acknowledged.")
        enqueue(feedback, SyncAction.ACK, actor)
    return f"Report #{feedback.pk} acknowledged."


def comment(feedback, actor, text) -> str:
    """`reports comment` — staff comment, mirrored to Discord + GitHub."""
    text = _clean(text, COMMENT_MAX)
    if not text:
        raise ValidationError("A comment cannot be empty.")
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        _add_comment(feedback, CommentSource.GAME, actor, text, is_staff=True)
        enqueue(feedback, SyncAction.COMMENT, actor, {"text": text})
    return f"Comment added to report #{feedback.pk}."


def set_progress(feedback, actor, note="") -> str:
    """`reports progress` — state → in_progress, clearing any closure fields."""
    note = _clean(note, NOTE_MAX)
    # No-op guard (mirrors set_state_internal): an identical target only spams
    # the timeline and re-fires side-effects, so short-circuit without writing.
    if feedback.state == FeedbackState.IN_PROGRESS:
        return f"Report #{feedback.pk} is already in progress."
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        # Mirror set_state_internal("in_progress"): clear all closure artifacts.
        feedback.state = FeedbackState.IN_PROGRESS
        feedback.resolution = None
        feedback.closed_by = None
        feedback.closed_at = None
        feedback.resolution_note = None
        feedback.duplicate_of = None
        feedback.save(update_fields=(
            "state", "resolution", "closed_by", "closed_at",
            "resolution_note", "duplicate_of",
        ))
        label = "Marked in progress" + (f": {note}" if note else "")
        add_system_comment(feedback, actor, f"{label}.")
        enqueue(feedback, SyncAction.PROGRESS, actor, {"note": note})
    return f"Report #{feedback.pk} marked in progress."


def close(feedback, actor, resolution, note="") -> str:
    """
    `reports resolve|wontfix|close` — state → closed with a resolution.
    `resolution` is one of fixed / wontfix / other; a generic close ('other')
    requires a non-empty reason (mirrors `rust_feedback_close`).
    """
    if resolution not in (
        FeedbackResolution.FIXED,
        FeedbackResolution.WONTFIX,
        FeedbackResolution.OTHER,
    ):
        raise ValidationError("Invalid resolution.")
    note = _clean(note, NOTE_MAX)
    if resolution == FeedbackResolution.OTHER and not note:
        raise ValidationError("A generic close requires a reason.")
    # No-op guard: re-closing with the SAME resolution is a no-op (re-closing
    # with a different resolution, e.g. wontfix -> fixed, is a real change).
    if feedback.state == FeedbackState.CLOSED and feedback.resolution == resolution:
        labels = {
            FeedbackResolution.FIXED: "resolved",
            FeedbackResolution.WONTFIX: "wontfix",
            FeedbackResolution.OTHER: "closed",
        }
        return f"Report #{feedback.pk} is already {labels[resolution]}."
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        feedback.state = FeedbackState.CLOSED
        feedback.resolution = resolution
        feedback.closed_by = actor
        feedback.closed_at = _now()
        feedback.resolution_note = note or None
        feedback.duplicate_of = None
        feedback.save(update_fields=(
            "state", "resolution", "closed_by", "closed_at",
            "resolution_note", "duplicate_of",
        ))
        labels = {
            FeedbackResolution.FIXED: "resolved",
            FeedbackResolution.WONTFIX: "wontfix",
            FeedbackResolution.OTHER: "closed",
        }
        label = f"Marked {labels[resolution]}" + (f": {note}" if note else "")
        add_system_comment(feedback, actor, f"{label}.")
        action = {
            FeedbackResolution.FIXED: SyncAction.RESOLVE,
            FeedbackResolution.WONTFIX: SyncAction.WONTFIX,
            FeedbackResolution.OTHER: SyncAction.CLOSE,
        }[resolution]
        enqueue(feedback, action, actor, {"note": note})
    return f"Report #{feedback.pk} {labels[resolution]}."


def mark_duplicate(feedback, actor, of_id) -> str:
    """`reports dupe` — close as a duplicate of another report."""
    try:
        of_id = int(of_id)
    except (TypeError, ValueError):
        raise ValidationError("A duplicate needs a valid target report ID.")
    if of_id == feedback.pk:
        raise ValidationError("A report cannot be a duplicate of itself.")
    if not Feedback.objects.filter(pk=of_id).exists():
        raise ValidationError(f"Report #{of_id} does not exist.")
    # No-op guard: already a duplicate of this same original (repointing to a
    # different original is a real change and is allowed through).
    if (
        feedback.state == FeedbackState.CLOSED
        and feedback.resolution == FeedbackResolution.DUPLICATE
        and feedback.duplicate_of_id == of_id
    ):
        return f"Report #{feedback.pk} is already a duplicate of #{of_id}."
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        feedback.state = FeedbackState.CLOSED
        feedback.resolution = FeedbackResolution.DUPLICATE
        feedback.closed_by = actor
        feedback.closed_at = _now()
        feedback.resolution_note = None
        feedback.duplicate_of_id = of_id
        feedback.save(update_fields=(
            "state", "resolution", "closed_by", "closed_at",
            "resolution_note", "duplicate_of",
        ))
        add_system_comment(feedback, actor, f"Marked duplicate of #{of_id}.")
        enqueue(feedback, SyncAction.DUPLICATE, actor, {"of_id": of_id})
    return f"Report #{feedback.pk} marked duplicate of #{of_id}."


def reopen(feedback, actor, note="") -> str:
    """`reports reopen` — state → open, wiping all closure artifacts."""
    note = _clean(note, NOTE_MAX)
    # No-op guard: an already-open report has nothing to reopen.
    if feedback.state == FeedbackState.OPEN:
        return f"Report #{feedback.pk} is already open."
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        feedback.state = FeedbackState.OPEN
        feedback.resolution = None
        feedback.closed_by = None
        feedback.closed_at = None
        feedback.resolution_note = None
        feedback.duplicate_of = None
        feedback.save(update_fields=(
            "state", "resolution", "closed_by", "closed_at",
            "resolution_note", "duplicate_of",
        ))
        label = "Reopened" + (f": {note}" if note else "")
        add_system_comment(feedback, actor, f"{label}.")
        enqueue(feedback, SyncAction.REOPEN, actor, {"note": note})
    return f"Report #{feedback.pk} reopened."


def bounty(feedback, actor, note="") -> str:
    """`reports bounty` — award a bounty (idempotent, single-award)."""
    note = _clean(note, NOTE_MAX)
    if feedback.bountied:
        return f"Report #{feedback.pk} bounty already awarded by {feedback.bountied_by}."
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        # Guarded update so a concurrent award can't double-apply.
        awarded = Feedback.objects.filter(pk=feedback.pk, bountied=False).update(
            bountied=True, bountied_by=actor, bountied_at=_now()
        )
        if not awarded:
            feedback.refresh_from_db(fields=("bountied", "bountied_by"))
            return f"Report #{feedback.pk} bounty already awarded by {feedback.bountied_by}."
        feedback.bountied = True
        feedback.bountied_by = actor
        label = "Bounty awarded" + (f": {note}" if note else "")
        add_system_comment(feedback, actor, f"{label}.")
        enqueue(feedback, SyncAction.BOUNTY, actor, {"note": note})
    return f"Bounty awarded on report #{feedback.pk}."


def promote(feedback, actor) -> str:
    """
    `reports promote` — file a GitHub issue. The website has no GitHub token, so
    it enqueues the intent for the daemon (which creates the issue and writes
    back `github_issue_url`). Private reports promote too: the tracker repo is
    private, so its issues are admin-only. The daemon's `build_issue_body`
    flags the private origin on the issue.
    """
    if feedback.is_promoted():
        return f"Report #{feedback.pk} already has a GitHub issue: {feedback.github_issue_url}"
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        enqueue(feedback, SyncAction.PROMOTE, actor)
    return f"Report #{feedback.pk} queued for GitHub promotion."


def assign_claude(feedback, actor, instructions="") -> str:
    """
    `reports claude` — ensure a GitHub issue exists and post the `@claude`
    assignment comment. Gods-only (enforced by the caller). Enqueued for the
    daemon, which owns the token, the issue creation, and the injection-guarded
    comment body (`assign_claude_comment`). Private reports are eligible — the
    tracker repo is private, so the issue and the `@claude` run stay admin-only.
    """
    instructions = _clean(instructions, INSTRUCTIONS_MAX)
    payload = {"instructions": instructions} if instructions else {}
    with transaction.atomic():
        _ack_if_needed(feedback, actor)
        enqueue(feedback, SyncAction.ASSIGN_CLAUDE, actor, payload)
    return f"Report #{feedback.pk} queued for Claude on GitHub."
