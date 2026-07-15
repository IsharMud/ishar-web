"""
Patch-notes web models — the web face of the game's in-game `news` command.

These map onto tables the **game** owns (Diesel migrations in
`isharmud/ishar-mud/rust-interop/migrations`), so every model here is
`managed = False`: Django reads and writes rows but never migrates the schema.

- `PatchNote` -> `patch_notes`: the note itself (draft or published).
- `PatchNoteSyncTask` -> `patch_notes_sync_queue`: the publish outbox the game
  drains to post the Discord announcement (the one side-effect the web container
  cannot do). See `docs/patch_notes_web_contract.md` in ishar-mud.

Per-account read state lives in `account_patch_notes_read`, whose composite
primary key `(account_id, patch_note_id)` does not map cleanly onto a Django
model — it is handled with raw SQL in `services.py`, mirroring the game's own
`patch_notes.rs` queries.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.unsigned import UnsignedAutoField


class PatchNote(models.Model):
    """A patch note (the game's "news"). Game-owned table; `managed = False`."""

    id = UnsignedAutoField(
        primary_key=True,
        db_column="id",
        verbose_name=_("Patch Note ID"),
    )
    title = models.CharField(
        max_length=80,
        db_column="title",
        help_text=_("Title of the patch note."),
        verbose_name=_("Title"),
    )
    body = models.TextField(
        db_column="body",
        help_text=_("Body (lightweight markdown: ## headers, - bullets, **bold**)."),
        verbose_name=_("Body"),
    )
    author = models.CharField(
        max_length=30,
        db_column="author",
        default="System",
        help_text=_("Author attribution shown to players."),
        verbose_name=_("Author"),
    )
    is_published = models.BooleanField(
        db_column="is_published",
        default=False,
        help_text=_("Published notes are visible to players; drafts are staff-only."),
        verbose_name=_("Published?"),
    )
    season_id = models.PositiveIntegerField(
        db_column="season_id",
        blank=True,
        null=True,
        help_text=_("Optional season this note belongs to."),
        verbose_name=_("Season"),
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        blank=True,
        null=True,
        help_text=_("When the draft was created."),
        verbose_name=_("Created At"),
    )
    published_at = models.DateTimeField(
        db_column="published_at",
        blank=True,
        null=True,
        help_text=_("When the note was published."),
        verbose_name=_("Published At"),
    )
    discord_sent_at = models.DateTimeField(
        db_column="discord_sent_at",
        blank=True,
        null=True,
        help_text=_("When the game posted the Discord announcement."),
        verbose_name=_("Discord Sent At"),
    )

    class Meta:
        managed = False
        db_table = "patch_notes"
        ordering = ("-published_at", "-created_at", "-id")
        verbose_name = _("Patch Note")
        verbose_name_plural = _("Patch Notes")

    def __str__(self) -> str:
        state = "published" if self.is_published else "draft"
        return f"#{self.pk} {self.title} ({state})"


class PatchNoteSyncTask(models.Model):
    """
    One queued publish side-effect for the game to replay (the Discord
    announcement). Game-owned outbox table; `managed = False`. The website
    writes `patch_notes` state directly and appends a row here in the same
    transaction (transactional outbox); the game's `patch_notes_sync_event`
    drains it. Contract: `docs/patch_notes_web_contract.md`.
    """

    class Action(models.TextChoices):
        PUBLISH = "publish", _("Publish")

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        DONE = "done", _("Done")
        ERROR = "error", _("Error")

    id = UnsignedAutoField(
        primary_key=True,
        db_column="id",
        verbose_name=_("Task ID"),
    )
    patch_note = models.ForeignKey(
        to=PatchNote,
        db_column="patch_note_id",
        to_field="id",
        on_delete=models.CASCADE,
        related_name="sync_tasks",
        related_query_name="sync_task",
        help_text=_("The note this side-effect concerns."),
        verbose_name=_("Patch Note"),
    )
    action = models.CharField(
        max_length=32,
        db_column="action",
        choices=Action,
        default=Action.PUBLISH,
        help_text=_("Semantic verb the game must replay."),
        verbose_name=_("Action"),
    )
    actor = models.CharField(
        max_length=64,
        db_column="actor",
        default="System",
        help_text=_("Staff attribution for the announcement."),
        verbose_name=_("Actor"),
    )
    status = models.CharField(
        max_length=16,
        db_column="status",
        choices=Status,
        default=Status.PENDING,
        help_text=_("Queue lifecycle: pending, done, or error."),
        verbose_name=_("Status"),
    )
    attempts = models.PositiveIntegerField(
        db_column="attempts",
        default=0,
        verbose_name=_("Attempts"),
    )
    last_error = models.CharField(
        max_length=255,
        db_column="last_error",
        blank=True,
        null=True,
        verbose_name=_("Last Error"),
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        blank=True,
        null=True,
        verbose_name=_("Created At"),
    )
    processed_at = models.DateTimeField(
        db_column="processed_at",
        blank=True,
        null=True,
        verbose_name=_("Processed At"),
    )

    class Meta:
        managed = False
        db_table = "patch_notes_sync_queue"
        ordering = ("id",)
        verbose_name = _("Patch Note Sync Task")
        verbose_name_plural = _("Patch Note Sync Tasks")

    def __str__(self) -> str:
        return f"{self.get_action_display()} on #{self.patch_note_id} ({self.status})"
