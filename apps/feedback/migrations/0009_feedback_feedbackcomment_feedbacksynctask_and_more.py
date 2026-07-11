"""
Retire the legacy website feedback board and introduce the game-owned feedback
triage models.

The old suggestion board (`FeedbackSubmission` on `feedback`, `FeedbackVote` on
`feedback_votes`) collided on the `feedback` table name with the new unified
in-game feedback system (ishar-mud #1737). Per the retirement decision, the
board is removed and this app is repurposed to triage the game tables.

**This migration issues no DDL.** The new `Feedback` / `FeedbackComment` /
`FeedbackSyncTask` models are `managed = False` (the game owns those tables), and
the teardown of the old models is wrapped in `SeparateDatabaseAndState` with
empty `database_operations`, so Django only forgets them in state — it never
drops the live `feedback` / `feedback_votes` tables. Reconciling any residual
legacy rows (and dropping the now-orphaned `feedback_votes` table) is a manual
DBA step, intentionally kept out of an automated live-DB migration.
"""
import apps.core.models.unsigned
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0008_remove_feedbackvote_one_vote_per_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    apps.core.models.unsigned.UnsignedAutoField(
                        db_column="id",
                        help_text="Auto-generated permanent feedback report ID.",
                        primary_key=True,
                        serialize=False,
                        verbose_name="Feedback ID",
                    ),
                ),
                (
                    "feedback_type",
                    models.CharField(
                        choices=[("bug", "Bug"), ("typo", "Typo"), ("idea", "Idea")],
                        db_column="feedback_type",
                        help_text="Kind of report: bug, typo, or idea.",
                        max_length=8,
                        verbose_name="Type",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[("game", "Game"), ("discord", "Discord")],
                        db_column="source",
                        default="game",
                        help_text="Where the report originated (in-game or Discord).",
                        max_length=8,
                        verbose_name="Source",
                    ),
                ),
                (
                    "player_name",
                    models.CharField(
                        blank=True,
                        db_column="player_name",
                        help_text="Player character name at filing time.",
                        max_length=64,
                        null=True,
                        verbose_name="Player Name",
                    ),
                ),
                (
                    "room_vnum",
                    models.IntegerField(
                        blank=True,
                        db_column="room_vnum",
                        help_text="Virtual number of the room the player filed from.",
                        null=True,
                        verbose_name="Room Vnum",
                    ),
                ),
                (
                    "player_level",
                    models.SmallIntegerField(
                        blank=True,
                        db_column="player_level",
                        help_text="Player level at filing time.",
                        null=True,
                        verbose_name="Player Level",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        db_column="body",
                        help_text="The report text as submitted by the player.",
                        verbose_name="Body",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("open", "Open"),
                            ("in_progress", "In Progress"),
                            ("closed", "Closed"),
                        ],
                        db_column="state",
                        default="open",
                        help_text="Lifecycle state: open, in progress, or closed.",
                        max_length=16,
                        verbose_name="State",
                    ),
                ),
                (
                    "resolution",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("fixed", "Fixed"),
                            ("wontfix", "Won't Fix"),
                            ("duplicate", "Duplicate"),
                            ("other", "Other"),
                        ],
                        db_column="resolution",
                        help_text="Closure reason (only set when closed).",
                        max_length=16,
                        null=True,
                        verbose_name="Resolution",
                    ),
                ),
                (
                    "closed_by",
                    models.CharField(
                        blank=True,
                        db_column="closed_by",
                        help_text="Staff member who closed the report.",
                        max_length=64,
                        null=True,
                        verbose_name="Closed By",
                    ),
                ),
                (
                    "resolution_note",
                    models.CharField(
                        blank=True,
                        db_column="resolution_note",
                        help_text="Optional note recorded at closure.",
                        max_length=255,
                        null=True,
                        verbose_name="Resolution Note",
                    ),
                ),
                (
                    "closed_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="closed_at",
                        help_text="When the report was closed.",
                        null=True,
                        verbose_name="Closed At",
                    ),
                ),
                (
                    "discord_thread_id",
                    models.PositiveBigIntegerField(
                        blank=True,
                        db_column="discord_thread_id",
                        help_text="Discord forum thread ID for this report.",
                        null=True,
                        verbose_name="Discord Thread ID",
                    ),
                ),
                (
                    "discord_message_id",
                    models.PositiveBigIntegerField(
                        blank=True,
                        db_column="discord_message_id",
                        help_text="Discord message ID for this report.",
                        null=True,
                        verbose_name="Discord Message ID",
                    ),
                ),
                (
                    "github_issue_url",
                    models.CharField(
                        blank=True,
                        db_column="github_issue_url",
                        help_text="GitHub issue URL, once the report is promoted.",
                        max_length=255,
                        null=True,
                        verbose_name="GitHub Issue URL",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="created_at",
                        help_text="When the report was filed.",
                        null=True,
                        verbose_name="Created At",
                    ),
                ),
                (
                    "discord_sent_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="discord_sent_at",
                        help_text="When the report was delivered to Discord (NULL = pending).",
                        null=True,
                        verbose_name="Discord Sent At",
                    ),
                ),
                (
                    "notified_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="notified_at",
                        help_text="Reserved for reporter notification.",
                        null=True,
                        verbose_name="Notified At",
                    ),
                ),
                (
                    "bountied",
                    models.BooleanField(
                        db_column="bountied",
                        default=False,
                        help_text="Whether a bounty has been awarded for this report.",
                        verbose_name="Bountied?",
                    ),
                ),
                (
                    "bountied_by",
                    models.CharField(
                        blank=True,
                        db_column="bountied_by",
                        help_text="Staff member who awarded the bounty.",
                        max_length=64,
                        null=True,
                        verbose_name="Bountied By",
                    ),
                ),
                (
                    "bountied_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="bountied_at",
                        help_text="When the bounty was awarded.",
                        null=True,
                        verbose_name="Bountied At",
                    ),
                ),
                (
                    "is_private",
                    models.BooleanField(
                        db_column="is_private",
                        default=False,
                        help_text="Private reports never reach Discord and cannot be promoted to a public GitHub issue (likely-exploit reports).",
                        verbose_name="Private?",
                    ),
                ),
                (
                    "acknowledged_by",
                    models.CharField(
                        blank=True,
                        db_column="acknowledged_by",
                        help_text="First staff member to claim the report.",
                        max_length=64,
                        null=True,
                        verbose_name="Acknowledged By",
                    ),
                ),
                (
                    "acknowledged_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="acknowledged_at",
                        help_text="When the report was acknowledged.",
                        null=True,
                        verbose_name="Acknowledged At",
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        db_column="account_id",
                        help_text="Account that filed the report, if known.",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="feedback_reports",
                        related_query_name="feedback_report",
                        to=settings.AUTH_USER_MODEL,
                        to_field="account_id",
                        verbose_name="Account",
                    ),
                ),
                (
                    "duplicate_of",
                    models.ForeignKey(
                        blank=True,
                        db_column="duplicate_of",
                        help_text="The report this one duplicates, when resolution=duplicate.",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="duplicates",
                        related_query_name="duplicate",
                        to="feedback.feedback",
                        verbose_name="Duplicate Of",
                    ),
                ),
            ],
            options={
                "verbose_name": "Feedback Report",
                "verbose_name_plural": "Feedback Reports",
                "db_table": "feedback",
                "ordering": ("-id",),
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="FeedbackComment",
            fields=[
                (
                    "id",
                    apps.core.models.unsigned.UnsignedAutoField(
                        db_column="id",
                        help_text="Auto-generated permanent comment ID.",
                        primary_key=True,
                        serialize=False,
                        verbose_name="Comment ID",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[
                            ("game", "Game"),
                            ("discord", "Discord"),
                            ("system", "System"),
                        ],
                        db_column="source",
                        default="game",
                        help_text="Origin of the comment: game, discord, or system.",
                        max_length=8,
                        verbose_name="Source",
                    ),
                ),
                (
                    "author",
                    models.CharField(
                        db_column="author",
                        help_text="Display name of the comment author.",
                        max_length=64,
                        verbose_name="Author",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        db_column="is_staff",
                        default=False,
                        help_text="Whether the author is staff.",
                        verbose_name="Staff?",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        db_column="body",
                        help_text="The comment text.",
                        verbose_name="Body",
                    ),
                ),
                (
                    "discord_message_id",
                    models.PositiveBigIntegerField(
                        blank=True,
                        db_column="discord_message_id",
                        help_text="Discord message ID, for Discord-sourced comments.",
                        null=True,
                        verbose_name="Discord Message ID",
                    ),
                ),
                (
                    "discord_author_id",
                    models.PositiveBigIntegerField(
                        blank=True,
                        db_column="discord_author_id",
                        help_text="Discord author ID, for Discord-sourced comments.",
                        null=True,
                        verbose_name="Discord Author ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="created_at",
                        help_text="When the comment was created.",
                        null=True,
                        verbose_name="Created At",
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        db_column="feedback_id",
                        help_text="The report this comment belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        related_query_name="comment",
                        to="feedback.feedback",
                        to_field="id",
                        verbose_name="Feedback Report",
                    ),
                ),
            ],
            options={
                "verbose_name": "Feedback Comment",
                "verbose_name_plural": "Feedback Comments",
                "db_table": "feedback_comments",
                "ordering": ("id",),
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="FeedbackSyncTask",
            fields=[
                (
                    "id",
                    apps.core.models.unsigned.UnsignedAutoField(
                        db_column="id",
                        primary_key=True,
                        serialize=False,
                        verbose_name="Task ID",
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("ack", "Acknowledge"),
                            ("comment", "Comment"),
                            ("progress", "Progress"),
                            ("resolve", "Resolve"),
                            ("wontfix", "Won't Fix"),
                            ("close", "Close"),
                            ("dupe", "Duplicate"),
                            ("reopen", "Reopen"),
                            ("bounty", "Bounty"),
                            ("promote", "Promote"),
                            ("assign_claude", "Assign to Claude"),
                        ],
                        db_column="action",
                        help_text="Semantic verb whose side-effects the daemon must replay.",
                        max_length=32,
                        verbose_name="Action",
                    ),
                ),
                (
                    "actor",
                    models.CharField(
                        db_column="actor",
                        help_text="Staff attribution for the side-effect.",
                        max_length=64,
                        verbose_name="Actor",
                    ),
                ),
                (
                    "payload",
                    models.JSONField(
                        blank=True,
                        db_column="payload",
                        help_text="Action parameters (note, reason, of_id, text, instructions).",
                        null=True,
                        verbose_name="Payload",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("done", "Done"),
                            ("error", "Error"),
                        ],
                        db_column="status",
                        default="pending",
                        help_text="Queue lifecycle: pending, done, or error.",
                        max_length=16,
                        verbose_name="Status",
                    ),
                ),
                (
                    "attempts",
                    models.PositiveIntegerField(
                        db_column="attempts",
                        default=0,
                        help_text="Number of times the daemon has attempted this task.",
                        verbose_name="Attempts",
                    ),
                ),
                (
                    "last_error",
                    models.CharField(
                        blank=True,
                        db_column="last_error",
                        help_text="Last error message, if the task failed.",
                        max_length=255,
                        null=True,
                        verbose_name="Last Error",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="created_at",
                        help_text="When the task was enqueued.",
                        null=True,
                        verbose_name="Created At",
                    ),
                ),
                (
                    "processed_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="processed_at",
                        help_text="When the daemon finished the task.",
                        null=True,
                        verbose_name="Processed At",
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        db_column="feedback_id",
                        help_text="The report this side-effect concerns.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sync_tasks",
                        related_query_name="sync_task",
                        to="feedback.feedback",
                        to_field="id",
                        verbose_name="Feedback Report",
                    ),
                ),
            ],
            options={
                "verbose_name": "Feedback Sync Task",
                "verbose_name_plural": "Feedback Sync Tasks",
                "db_table": "feedback_sync_queue",
                "ordering": ("id",),
                "managed": False,
            },
        ),
        # Retire the legacy board from Django's state ONLY — no DROP TABLE runs
        # against the live database (database_operations is empty).
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="feedbackvote",
                    name="feedback_submission",
                ),
                migrations.AlterUniqueTogether(
                    name="feedbackvote",
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name="feedbackvote",
                    name="account",
                ),
                migrations.DeleteModel(name="FeedbackSubmission"),
                migrations.DeleteModel(name="FeedbackVote"),
            ],
            database_operations=[],
        ),
    ]
