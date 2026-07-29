"""
Immortal Trial application flow: three site-owned tables — applications,
their comment/audit timeline, and the `trial_sync_queue` side-effect outbox
the host daemon drains to Discord. The account FK is Django-level only
(`db_constraint=False`): no DDL touches the game-owned `accounts` table.
The unique constraint on `open_slot` is the MariaDB stand-in for a
conditional "one open application per account" constraint (NULLs don't
collide; the column is NULLed on terminal transitions).
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TrialApplication",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Application ID"
                    ),
                ),
                (
                    "character_name",
                    models.CharField(
                        help_text="The mortal character the applicant is known by.",
                        max_length=64,
                        verbose_name="Character Name",
                    ),
                ),
                (
                    "track",
                    models.CharField(
                        choices=[("zoner", "Zoner"), ("coder", "Coder")],
                        max_length=8,
                        verbose_name="Track",
                    ),
                ),
                (
                    "proposal",
                    models.TextField(
                        help_text="The trial project pitch: small, guided, ~4 weeks.",
                        verbose_name="Project Proposal",
                    ),
                ),
                (
                    "experience",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Relevant building / coding / writing experience.",
                        verbose_name="Experience",
                    ),
                ),
                (
                    "ack_ai_policy",
                    models.BooleanField(
                        default=False,
                        help_text="Acknowledged: trial-phase creative writing must be original work.",
                        verbose_name="AI Policy Acknowledged",
                    ),
                ),
                (
                    "ack_commitment",
                    models.BooleanField(
                        default=False,
                        help_text="Acknowledged: the time and communication commitment.",
                        verbose_name="Commitment Acknowledged",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("submitted", "Under Review"),
                            ("needs_revision", "Needs Revision"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                            ("withdrawn", "Withdrawn"),
                        ],
                        default="submitted",
                        max_length=16,
                        verbose_name="Status",
                    ),
                ),
                (
                    "open_slot",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Open Slot"
                    ),
                ),
                (
                    "submitted_at",
                    models.DateTimeField(
                        help_text="Reset on resubmission; starts the review clock.",
                        verbose_name="Submitted At",
                    ),
                ),
                (
                    "due_at",
                    models.DateTimeField(
                        help_text="submitted_at + 7 days. Display-only review deadline.",
                        verbose_name="Review Due At",
                    ),
                ),
                (
                    "revision_count",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Revisions"
                    ),
                ),
                (
                    "decided_by",
                    models.CharField(
                        blank=True,
                        help_text="Staff attribution for the decision.",
                        max_length=64,
                        null=True,
                        verbose_name="Decided By",
                    ),
                ),
                (
                    "decided_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Decided At"
                    ),
                ),
                (
                    "rejection_reason",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Rejection Reason",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "account",
                    models.ForeignKey(
                        db_column="account_id",
                        db_constraint=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trial_applications",
                        related_query_name="trial_application",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Account",
                    ),
                ),
            ],
            options={
                "verbose_name": "Trial Application",
                "verbose_name_plural": "Trial Applications",
                "db_table": "trial_applications",
                "ordering": ("due_at", "-id"),
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="TrialComment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Comment ID"
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("staff", "Staff"),
                            ("applicant", "Applicant"),
                            ("system", "System"),
                        ],
                        max_length=16,
                        verbose_name="Kind",
                    ),
                ),
                (
                    "is_internal",
                    models.BooleanField(
                        default=False,
                        help_text="Staff-only: never shown to the applicant, never echoed to Discord.",
                        verbose_name="Internal?",
                    ),
                ),
                (
                    "author",
                    models.CharField(
                        help_text="Staff name, or the applicant's character/account name.",
                        max_length=64,
                        verbose_name="Author",
                    ),
                ),
                ("body", models.TextField(verbose_name="Body")),
                ("created_at", models.DateTimeField(verbose_name="Created At")),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        related_query_name="comment",
                        to="trials.trialapplication",
                        verbose_name="Application",
                    ),
                ),
            ],
            options={
                "verbose_name": "Trial Comment",
                "verbose_name_plural": "Trial Comments",
                "db_table": "trial_comments",
                "ordering": ("id",),
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="TrialSyncTask",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Task ID"
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("submitted", "Submitted"),
                            ("resubmitted", "Resubmitted"),
                            ("comment", "Comment"),
                            ("reply", "Reply"),
                            ("needs_revision", "Needs Revision"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                            ("withdrawn", "Withdrawn"),
                        ],
                        help_text="Semantic verb whose side-effects the daemon must replay.",
                        max_length=32,
                        verbose_name="Action",
                    ),
                ),
                (
                    "actor",
                    models.CharField(
                        help_text="Attribution for the side-effect.",
                        max_length=64,
                        verbose_name="Actor",
                    ),
                ),
                (
                    "payload",
                    models.JSONField(
                        blank=True,
                        help_text="Action parameters (see module docstring).",
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
                        default="pending",
                        max_length=16,
                        verbose_name="Status",
                    ),
                ),
                (
                    "attempts",
                    models.PositiveIntegerField(default=0, verbose_name="Attempts"),
                ),
                (
                    "last_error",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Last Error"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Created At"
                    ),
                ),
                (
                    "processed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Processed At"
                    ),
                ),
                (
                    "application",
                    models.ForeignKey(
                        db_column="application_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sync_tasks",
                        related_query_name="sync_task",
                        to="trials.trialapplication",
                        verbose_name="Application",
                    ),
                ),
            ],
            options={
                "verbose_name": "Trial Sync Task",
                "verbose_name_plural": "Trial Sync Tasks",
                "db_table": "trial_sync_queue",
                "ordering": ("id",),
                "managed": True,
            },
        ),
        migrations.AddConstraint(
            model_name="trialapplication",
            constraint=models.UniqueConstraint(
                fields=("open_slot",), name="one_open_application_per_account"
            ),
        ),
    ]
