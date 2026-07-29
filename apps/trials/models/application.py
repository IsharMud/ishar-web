"""
Immortal Trial applications — the site-owned intake for the trial process
described at /trials/ (immortal_policy): a player pitches a small ~4-week
project on one of two tracks, Eternal+ staff review inside a 7-day window,
and acceptance grants Immortal (Trial) rank.
"""
from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.accounts.models import Account

from .choices import OPEN_STATUSES, TrialStatus, TrialTrack

REVIEW_WINDOW = timedelta(days=7)


class TrialApplication(models.Model):
    """One application to the Immortal Trial."""

    id = models.AutoField(
        primary_key=True,
        verbose_name="Application ID",
    )
    account = models.ForeignKey(
        to=Account,
        db_column="account_id",
        to_field="account_id",
        db_constraint=False,
        on_delete=models.CASCADE,
        related_name="trial_applications",
        related_query_name="trial_application",
        verbose_name="Account",
    )
    character_name = models.CharField(
        max_length=64,
        help_text="The mortal character the applicant is known by.",
        verbose_name="Character Name",
    )
    track = models.CharField(
        max_length=8,
        choices=TrialTrack,
        verbose_name="Track",
    )
    proposal = models.TextField(
        help_text="The trial project pitch: small, guided, ~4 weeks.",
        verbose_name="Project Proposal",
    )
    experience = models.TextField(
        blank=True,
        default="",
        help_text="Relevant building / coding / writing experience.",
        verbose_name="Experience",
    )
    ack_ai_policy = models.BooleanField(
        default=False,
        help_text="Acknowledged: trial-phase creative writing must be original work.",
        verbose_name="AI Policy Acknowledged",
    )
    ack_commitment = models.BooleanField(
        default=False,
        help_text="Acknowledged: the time and communication commitment.",
        verbose_name="Commitment Acknowledged",
    )
    status = models.CharField(
        max_length=16,
        choices=TrialStatus,
        default=TrialStatus.SUBMITTED,
        verbose_name="Status",
    )
    # MariaDB has no conditional unique constraints, so "one open application
    # per account" is enforced by mirroring account_id here while the
    # application is open and NULLing it on any terminal transition — NULLs
    # never collide in a unique index.
    open_slot = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Open Slot",
    )
    submitted_at = models.DateTimeField(
        help_text="Reset on resubmission; starts the review clock.",
        verbose_name="Submitted At",
    )
    due_at = models.DateTimeField(
        help_text="submitted_at + 7 days. Display-only review deadline.",
        verbose_name="Review Due At",
    )
    revision_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Revisions",
    )
    decided_by = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Staff attribution for the decision.",
        verbose_name="Decided By",
    )
    decided_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Decided At",
    )
    rejection_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Rejection Reason",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )

    class Meta:
        managed = True
        db_table = "trial_applications"
        constraints = (
            models.UniqueConstraint(
                fields=("open_slot",),
                name="one_open_application_per_account",
            ),
        )
        ordering = ("due_at", "-id")
        verbose_name = "Trial Application"
        verbose_name_plural = "Trial Applications"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: #{self.pk} ({self.status})"

    def __str__(self) -> str:
        return f"#{self.pk} {self.character_name} [{self.get_track_display()}]"

    # -- Predicates -------------------------------------------------------

    def is_open(self) -> bool:
        return self.status in OPEN_STATUSES

    def is_submitted(self) -> bool:
        return self.status == TrialStatus.SUBMITTED

    def is_needs_revision(self) -> bool:
        return self.status == TrialStatus.NEEDS_REVISION

    def is_accepted(self) -> bool:
        return self.status == TrialStatus.ACCEPTED

    def is_rejected(self) -> bool:
        return self.status == TrialStatus.REJECTED

    def is_terminal(self) -> bool:
        return not self.is_open()

    def is_overdue(self) -> bool:
        """Under review past the 7-day window — a promise staff missed."""
        return self.is_submitted() and self.due_at < timezone.now()

    # -- Presentation -----------------------------------------------------

    @property
    def days_left(self) -> int:
        """Whole days until (positive) or past (negative) the review deadline."""
        return (self.due_at - timezone.now()).days

    @property
    def due_label(self) -> str:
        """Compact clock pill text — pills don't wrap, so keep it short."""
        if self.is_overdue():
            days = -self.days_left
            return f"overdue {days}d" if days else "overdue"
        days = self.days_left
        return f"due in {days}d" if days > 0 else "due today"

    def summary(self, length: int = 80) -> str:
        line = (self.proposal or "").strip().splitlines()
        line = line[0] if line else ""
        if len(line) > length:
            line = line[: length - 1].rstrip() + "…"
        return line or "(no text)"

    @property
    def track_icon(self) -> str:
        """Bootstrap-icons name for the track."""
        return {
            TrialTrack.ZONER: "map",
            TrialTrack.CODER: "code-slash",
        }.get(self.track, "stars")

    @property
    def status_label(self) -> str:
        return self.get_status_display()

    @property
    def status_css(self) -> str:
        """Bootstrap contextual class for the status."""
        return {
            TrialStatus.SUBMITTED: "info",
            TrialStatus.NEEDS_REVISION: "warning",
            TrialStatus.ACCEPTED: "success",
            TrialStatus.REJECTED: "danger",
            TrialStatus.WITHDRAWN: "secondary",
        }.get(self.status, "secondary")

    @property
    def status_pill(self) -> str:
        """Admin Console pill modifier (.ac-pill--*) for the status."""
        return {
            TrialStatus.SUBMITTED: "info",
            TrialStatus.NEEDS_REVISION: "warn",
            TrialStatus.ACCEPTED: "ok",
            TrialStatus.REJECTED: "danger",
            TrialStatus.WITHDRAWN: "muted",
        }.get(self.status, "muted")
