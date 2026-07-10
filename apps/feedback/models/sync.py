"""
Feedback side-effect outbox (`feedback_sync_queue` table).

The website owns authoritative **state** in the shared DB (it writes the
`feedback` / `feedback_comments` rows directly, so both the dashboard and the
in-game `reports` list reflect a change instantly). What the website cannot do
is the **networked side-effects** the in-game command fires inline: Discord
thread echoes, GitHub issue creation, GitHub state sync, and the `@claude`
assignment comment (these need the game host's Discord webhooks and
`GITHUB_TOKEN`).

So each staff action enqueues one row here describing the semantic verb + its
parameters. A host daemon (separate workflow) drains `status='pending'` rows and
replays the exact Discord/GitHub side-effects the in-game command would, reusing
the Rust logic in `feedback.rs` — no presentation logic is duplicated in Python.

The table is game/daemon-owned, so this model is `managed = False`. See
`docs/feedback_sync_contract.md` in ishar-mud for the wire contract.
"""
from django.db import models

from .choices import SyncAction, SyncStatus
from .feedback import Feedback


class FeedbackSyncTask(models.Model):
    """One queued side-effect intent for the host daemon to replay."""

    id = models.BigAutoField(
        primary_key=True,
        db_column="id",
        verbose_name="Task ID",
    )
    feedback = models.ForeignKey(
        to=Feedback,
        db_column="feedback_id",
        to_field="id",
        on_delete=models.CASCADE,
        related_name="sync_tasks",
        related_query_name="sync_task",
        help_text="The report this side-effect concerns.",
        verbose_name="Feedback Report",
    )
    action = models.CharField(
        max_length=32,
        db_column="action",
        choices=SyncAction,
        help_text="Semantic verb whose side-effects the daemon must replay.",
        verbose_name="Action",
    )
    actor = models.CharField(
        max_length=64,
        db_column="actor",
        help_text="Staff attribution for the side-effect.",
        verbose_name="Actor",
    )
    payload = models.JSONField(
        db_column="payload",
        blank=True,
        null=True,
        help_text="Action parameters (note, reason, of_id, text, instructions).",
        verbose_name="Payload",
    )
    status = models.CharField(
        max_length=16,
        db_column="status",
        choices=SyncStatus,
        default=SyncStatus.PENDING,
        help_text="Queue lifecycle: pending, done, or error.",
        verbose_name="Status",
    )
    attempts = models.PositiveIntegerField(
        db_column="attempts",
        default=0,
        help_text="Number of times the daemon has attempted this task.",
        verbose_name="Attempts",
    )
    last_error = models.CharField(
        max_length=255,
        db_column="last_error",
        blank=True,
        null=True,
        help_text="Last error message, if the task failed.",
        verbose_name="Last Error",
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        blank=True,
        null=True,
        help_text="When the task was enqueued.",
        verbose_name="Created At",
    )
    processed_at = models.DateTimeField(
        db_column="processed_at",
        blank=True,
        null=True,
        help_text="When the daemon finished the task.",
        verbose_name="Processed At",
    )

    class Meta:
        managed = False
        db_table = "feedback_sync_queue"
        ordering = ("id",)
        verbose_name = "Feedback Sync Task"
        verbose_name_plural = "Feedback Sync Tasks"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.action} #{self.feedback_id}"

    def __str__(self) -> str:
        return f"{self.get_action_display()} on #{self.feedback_id} ({self.status})"
