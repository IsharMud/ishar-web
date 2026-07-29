"""
Trial side-effect outbox (`trial_sync_queue` table).

Same transactional-outbox split as feedback: the site owns authoritative state
(application rows, comments), and each action enqueues one row here for the
host daemon to replay as a staff-Discord post. Unlike `feedback_sync_queue`
(game/daemon-owned, frozen contract), this table is **site-owned** — this
docstring is the source of truth for its wire contract:

The daemon polls `status='pending'` rows ordered by `id`, posts one staff
Discord embed per row, then sets `done` (or `error` + `last_error`), stamping
`processed_at` and bumping `attempts`. Link target for application rows:
`/trials/review/<application_id>/`. Payloads by action:

- submitted / resubmitted: {"track", "character_name", "eligible", "seasons", "remorts"}
- comment (applicant-facing staff comment; internal comments are NEVER enqueued): {"text"}
- reply (applicant reply): {"text"}
- needs_revision: {"note"}
- accepted: {"granted": bool}   # whether immortal_level was actually written
- rejected: {"reason"}
- withdrawn: {}

Until the daemon-side worker ships (tracked in ishar-mud), rows accumulate
harmlessly as `pending` — the same rollout property the feedback queue had.
"""
from django.db import models

from .application import TrialApplication
from .choices import TrialSyncAction, TrialSyncStatus


class TrialSyncTask(models.Model):
    """One queued side-effect intent for the host daemon to replay."""

    id = models.AutoField(
        primary_key=True,
        verbose_name="Task ID",
    )
    application = models.ForeignKey(
        to=TrialApplication,
        db_column="application_id",
        on_delete=models.CASCADE,
        related_name="sync_tasks",
        related_query_name="sync_task",
        verbose_name="Application",
    )
    action = models.CharField(
        max_length=32,
        choices=TrialSyncAction,
        help_text="Semantic verb whose side-effects the daemon must replay.",
        verbose_name="Action",
    )
    actor = models.CharField(
        max_length=64,
        help_text="Attribution for the side-effect.",
        verbose_name="Actor",
    )
    payload = models.JSONField(
        blank=True,
        null=True,
        help_text="Action parameters (see module docstring).",
        verbose_name="Payload",
    )
    status = models.CharField(
        max_length=16,
        choices=TrialSyncStatus,
        default=TrialSyncStatus.PENDING,
        verbose_name="Status",
    )
    attempts = models.PositiveIntegerField(
        default=0,
        verbose_name="Attempts",
    )
    last_error = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Last Error",
    )
    created_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Created At",
    )
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Processed At",
    )

    class Meta:
        managed = True
        db_table = "trial_sync_queue"
        ordering = ("id",)
        verbose_name = "Trial Sync Task"
        verbose_name_plural = "Trial Sync Tasks"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.action} #{self.application_id}"

    def __str__(self) -> str:
        return f"{self.get_action_display()} on #{self.application_id} ({self.status})"
