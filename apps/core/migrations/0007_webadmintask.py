"""
Register the game-owned `web_admin_queue` outbox model.

**This migration issues no DDL.** `WebAdminTask` is `managed = False` — the
table is created game-side by the ishar-mud rust-interop migration
`2026-07-12-000000-0000_web_admin_queue`, which must be applied (a game
deploy) before the events/season consoles can enqueue. See
`docs/web_bridge_contracts.md` in ishar-mud.
"""
import apps.core.models.unsigned
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebAdminTask",
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
                    "command",
                    models.CharField(
                        choices=[
                            ("event_start", "Start/Extend Event"),
                            ("event_end", "End Event"),
                            ("season_set_expiration", "Set Season Expiration"),
                            ("season_set_auto_cycle", "Set Season Auto-Cycle"),
                            ("season_cycle", "Cycle Season"),
                            ("season_start", "Start Season"),
                        ],
                        db_column="command",
                        help_text="Semantic verb the game executes.",
                        max_length=32,
                        verbose_name="Command",
                    ),
                ),
                (
                    "payload",
                    models.JSONField(
                        blank=True,
                        db_column="payload",
                        help_text=(
                            "Verb parameters: {event_type?, duration_seconds?,"
                            " expiration_date?, enabled?}."
                        ),
                        null=True,
                        verbose_name="Payload",
                    ),
                ),
                (
                    "actor_account",
                    models.PositiveIntegerField(
                        db_column="actor_account",
                        help_text=(
                            "accounts.account_id of the staff member; the game"
                            " re-checks its immortal_level against the verb's"
                            " privilege floor."
                        ),
                        verbose_name="Actor Account ID",
                    ),
                ),
                (
                    "actor_name",
                    models.CharField(
                        db_column="actor_name",
                        help_text="Staff attribution (immortal character name).",
                        max_length=64,
                        verbose_name="Actor",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("done", "Done"),
                            ("error", "Error"),
                            ("cancelled", "Cancelled"),
                        ],
                        db_column="status",
                        default="pending",
                        max_length=16,
                        verbose_name="Status",
                    ),
                ),
                (
                    "attempts",
                    models.PositiveIntegerField(
                        db_column="attempts",
                        default=0,
                        verbose_name="Attempts",
                    ),
                ),
                (
                    "result",
                    models.CharField(
                        blank=True,
                        db_column="result",
                        help_text=(
                            "Human-readable outcome (or error) written by the"
                            " game."
                        ),
                        max_length=255,
                        null=True,
                        verbose_name="Result",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="created_at",
                        null=True,
                        verbose_name="Created At",
                    ),
                ),
                (
                    "processed_at",
                    models.DateTimeField(
                        blank=True,
                        db_column="processed_at",
                        null=True,
                        verbose_name="Processed At",
                    ),
                ),
            ],
            options={
                "verbose_name": "Web Admin Task",
                "verbose_name_plural": "Web Admin Tasks",
                "db_table": "web_admin_queue",
                "ordering": ("-id",),
                "managed": False,
            },
        ),
    ]
