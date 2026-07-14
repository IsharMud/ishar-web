"""
Read/triage model for the in-game feedback report (`feedback` table).

The table is owned by the game (created and evolved by ishar-mud
`rust-interop/migrations/*feedback*`), so this model is **`managed = False`** —
Django never issues DDL against it. State mutations from the website are made
through `apps.feedback.services`, which mirrors the Rust `set_state_internal`
state machine exactly and enqueues the network side-effects for the host daemon.
"""
from django.db import models

from apps.accounts.models import Account
from apps.core.models.unsigned import UnsignedAutoField

from .choices import (
    FeedbackResolution,
    FeedbackSource,
    FeedbackState,
    FeedbackType,
)


class Feedback(models.Model):
    """A single player feedback report (bug / typo / idea)."""

    id = UnsignedAutoField(
        primary_key=True,
        db_column="id",
        help_text="Auto-generated permanent feedback report ID.",
        verbose_name="Feedback ID",
    )
    feedback_type = models.CharField(
        max_length=8,
        db_column="feedback_type",
        choices=FeedbackType,
        help_text="Kind of report: bug, typo, or idea.",
        verbose_name="Type",
    )
    source = models.CharField(
        max_length=8,
        db_column="source",
        choices=FeedbackSource,
        default=FeedbackSource.GAME,
        help_text="Where the report originated (in-game or Discord).",
        verbose_name="Source",
    )
    account = models.ForeignKey(
        to=Account,
        db_column="account_id",
        to_field="account_id",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="feedback_reports",
        related_query_name="feedback_report",
        help_text="Account that filed the report, if known.",
        verbose_name="Account",
    )
    player_name = models.CharField(
        max_length=64,
        db_column="player_name",
        blank=True,
        null=True,
        help_text="Player character name at filing time.",
        verbose_name="Player Name",
    )
    room_vnum = models.IntegerField(
        db_column="room_vnum",
        blank=True,
        null=True,
        help_text="Virtual number of the room the player filed from.",
        verbose_name="Room Vnum",
    )
    player_level = models.SmallIntegerField(
        db_column="player_level",
        blank=True,
        null=True,
        help_text="Player level at filing time.",
        verbose_name="Player Level",
    )
    body = models.TextField(
        db_column="body",
        help_text="The report text as submitted by the player.",
        verbose_name="Body",
    )
    state = models.CharField(
        max_length=16,
        db_column="state",
        choices=FeedbackState,
        default=FeedbackState.OPEN,
        help_text="Lifecycle state: open, in progress, or closed.",
        verbose_name="State",
    )
    resolution = models.CharField(
        max_length=16,
        db_column="resolution",
        choices=FeedbackResolution,
        blank=True,
        null=True,
        help_text="Closure reason (only set when closed).",
        verbose_name="Resolution",
    )
    closed_by = models.CharField(
        max_length=64,
        db_column="closed_by",
        blank=True,
        null=True,
        help_text="Staff member who closed the report.",
        verbose_name="Closed By",
    )
    resolution_note = models.CharField(
        max_length=255,
        db_column="resolution_note",
        blank=True,
        null=True,
        help_text="Optional note recorded at closure.",
        verbose_name="Resolution Note",
    )
    closed_at = models.DateTimeField(
        db_column="closed_at",
        blank=True,
        null=True,
        help_text="When the report was closed.",
        verbose_name="Closed At",
    )
    duplicate_of = models.ForeignKey(
        to="self",
        db_column="duplicate_of",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="duplicates",
        related_query_name="duplicate",
        help_text="The report this one duplicates, when resolution=duplicate.",
        verbose_name="Duplicate Of",
    )
    discord_thread_id = models.PositiveBigIntegerField(
        db_column="discord_thread_id",
        blank=True,
        null=True,
        help_text="Discord forum thread ID for this report.",
        verbose_name="Discord Thread ID",
    )
    discord_message_id = models.PositiveBigIntegerField(
        db_column="discord_message_id",
        blank=True,
        null=True,
        help_text="Discord message ID for this report.",
        verbose_name="Discord Message ID",
    )
    github_issue_url = models.CharField(
        max_length=255,
        db_column="github_issue_url",
        blank=True,
        null=True,
        help_text="GitHub issue URL, once the report is promoted.",
        verbose_name="GitHub Issue URL",
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        blank=True,
        null=True,
        help_text="When the report was filed.",
        verbose_name="Created At",
    )
    discord_sent_at = models.DateTimeField(
        db_column="discord_sent_at",
        blank=True,
        null=True,
        help_text="When the report was delivered to Discord (NULL = pending).",
        verbose_name="Discord Sent At",
    )
    notified_at = models.DateTimeField(
        db_column="notified_at",
        blank=True,
        null=True,
        help_text="Reserved for reporter notification.",
        verbose_name="Notified At",
    )
    bountied = models.BooleanField(
        db_column="bountied",
        default=False,
        help_text="Whether a bounty has been awarded for this report.",
        verbose_name="Bountied?",
    )
    bountied_by = models.CharField(
        max_length=64,
        db_column="bountied_by",
        blank=True,
        null=True,
        help_text="Staff member who awarded the bounty.",
        verbose_name="Bountied By",
    )
    bountied_at = models.DateTimeField(
        db_column="bountied_at",
        blank=True,
        null=True,
        help_text="When the bounty was awarded.",
        verbose_name="Bountied At",
    )
    is_private = models.BooleanField(
        db_column="is_private",
        default=False,
        help_text=(
            "Private reports never reach Discord (likely-exploit reports). They "
            "can still be promoted to the private GitHub tracker, where issues "
            "stay admin-only."
        ),
        verbose_name="Private?",
    )
    acknowledged_by = models.CharField(
        max_length=64,
        db_column="acknowledged_by",
        blank=True,
        null=True,
        help_text="First staff member to claim the report.",
        verbose_name="Acknowledged By",
    )
    acknowledged_at = models.DateTimeField(
        db_column="acknowledged_at",
        blank=True,
        null=True,
        help_text="When the report was acknowledged.",
        verbose_name="Acknowledged At",
    )

    class Meta:
        managed = False
        db_table = "feedback"
        ordering = ("-id",)
        verbose_name = "Feedback Report"
        verbose_name_plural = "Feedback Reports"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: #{self.pk} ({self.feedback_type})"

    def __str__(self) -> str:
        return f"#{self.pk} [{self.get_feedback_type_display()}] {self.summary()}"

    # -- Predicates -------------------------------------------------------

    def is_open(self) -> bool:
        return self.state == FeedbackState.OPEN

    def is_in_progress(self) -> bool:
        return self.state == FeedbackState.IN_PROGRESS

    def is_closed(self) -> bool:
        return self.state == FeedbackState.CLOSED

    def is_active(self) -> bool:
        """Open or in-progress — i.e. not closed (mirrors `fetch_reports`)."""
        return self.state in (FeedbackState.OPEN, FeedbackState.IN_PROGRESS)

    def is_acknowledged(self) -> bool:
        return bool(self.acknowledged_by)

    def is_unacknowledged(self) -> bool:
        """Open + never claimed — the in-game "needs attention" marker."""
        return self.is_open() and not self.acknowledged_by

    def is_promoted(self) -> bool:
        return bool(self.github_issue_url)

    def is_bug(self) -> bool:
        return self.feedback_type == FeedbackType.BUG

    # -- Presentation -----------------------------------------------------

    def summary(self, length: int = 80) -> str:
        """First line of the body, truncated — matches `summary_line`."""
        line = (self.body or "").strip().splitlines()
        line = line[0] if line else ""
        if len(line) > length:
            line = line[: length - 1].rstrip() + "…"
        return line or "(no text)"

    @property
    def type_icon(self) -> str:
        """Bootstrap-icons name for the report type."""
        return {
            FeedbackType.BUG: "bug",
            FeedbackType.TYPO: "pencil",
            FeedbackType.IDEA: "lightbulb",
        }.get(self.feedback_type, "flag")

    @property
    def status_label(self) -> str:
        """Human status combining state + resolution (matches `status_tag`)."""
        if self.is_open():
            return "Open"
        if self.is_in_progress():
            return "In Progress"
        if self.resolution == FeedbackResolution.FIXED:
            return "Resolved"
        if self.resolution == FeedbackResolution.WONTFIX:
            return "Won't Fix"
        if self.resolution == FeedbackResolution.DUPLICATE:
            if self.duplicate_of_id:
                return f"Duplicate of #{self.duplicate_of_id}"
            return "Duplicate"
        return "Closed"

    @property
    def status_css(self) -> str:
        """Bootstrap contextual class for the status badge."""
        if self.is_open():
            return "success" if self.is_acknowledged() else "danger"
        if self.is_in_progress():
            return "info"
        if self.resolution == FeedbackResolution.FIXED:
            return "primary"
        if self.resolution == FeedbackResolution.WONTFIX:
            return "danger"
        if self.resolution == FeedbackResolution.DUPLICATE:
            return "warning"
        return "secondary"

    @property
    def status_pill(self) -> str:
        """Admin Console pill modifier (.ac-pill--*) for the status."""
        if self.is_open():
            return "ok" if self.is_acknowledged() else "danger"
        if self.is_in_progress():
            return "info"
        if self.resolution == FeedbackResolution.FIXED:
            return "accent"
        if self.resolution == FeedbackResolution.WONTFIX:
            return "danger"
        if self.resolution == FeedbackResolution.DUPLICATE:
            return "warn"
        return "muted"
