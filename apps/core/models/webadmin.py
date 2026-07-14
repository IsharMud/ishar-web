"""
Web admin command outbox (`web_admin_queue` table).

The game loads `global_event` and `seasons` at boot only, so the website
cannot write that state directly — a Django UPDATE would be invisible to the
running game until a reboot. Instead the staff consoles (events, season)
enqueue an *intent* here; the game drains one command per game-minute,
validates it (verb, parameter bounds, and a re-check of the enqueuing
account's `immortal_level` against the verb's privilege floor), executes it
through its own entry points, and writes `status`/`result` back for the
console to poll. Rows are never deleted — the table is the admin audit log.

The table is game-owned (rust-interop migration
`2026-07-12-000000-0000_web_admin_queue`), so this model is `managed = False`
and the command/status strings are a contract that must not drift. See
`docs/web_bridge_contracts.md` in ishar-mud.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from .unsigned import UnsignedAutoField


class WebAdminCommand(models.TextChoices):
    """`web_admin_queue.command` — semantic verbs the game executes."""

    EVENT_START = "event_start", _("Start/Extend Event")
    EVENT_END = "event_end", _("End Event")
    SEASON_SET_EXPIRATION = "season_set_expiration", _("Set Season Expiration")
    SEASON_SET_AUTO_CYCLE = "season_set_auto_cycle", _("Set Season Auto-Cycle")
    SEASON_CYCLE = "season_cycle", _("Cycle Season")
    SEASON_START = "season_start", _("Start Season")
    REBOOT_NOTICE = "reboot_notice", _("Announce Scheduled Reboot")
    REBOOT_CANCEL = "reboot_cancel", _("Cancel Scheduled Reboot")


class WebAdminStatus(models.TextChoices):
    """`web_admin_queue.status` ENUM('pending','done','error','cancelled')."""

    PENDING = "pending", _("Pending")
    DONE = "done", _("Done")
    ERROR = "error", _("Error")
    CANCELLED = "cancelled", _("Cancelled")


class WebAdminTask(models.Model):
    """One queued admin command for the game to execute."""

    id = UnsignedAutoField(
        primary_key=True,
        db_column="id",
        verbose_name="Task ID",
    )
    command = models.CharField(
        max_length=32,
        db_column="command",
        choices=WebAdminCommand,
        help_text="Semantic verb the game executes.",
        verbose_name="Command",
    )
    payload = models.JSONField(
        db_column="payload",
        blank=True,
        null=True,
        help_text=(
            "Verb parameters:"
            " {event_type?, duration_seconds?, expiration_date?, enabled?}."
        ),
        verbose_name="Payload",
    )
    actor_account = models.PositiveIntegerField(
        db_column="actor_account",
        help_text=(
            "accounts.account_id of the staff member; the game re-checks"
            " its immortal_level against the verb's privilege floor."
        ),
        verbose_name="Actor Account ID",
    )
    actor_name = models.CharField(
        max_length=64,
        db_column="actor_name",
        help_text="Staff attribution (immortal character name).",
        verbose_name="Actor",
    )
    status = models.CharField(
        max_length=16,
        db_column="status",
        choices=WebAdminStatus,
        default=WebAdminStatus.PENDING,
        verbose_name="Status",
    )
    attempts = models.PositiveIntegerField(
        db_column="attempts",
        default=0,
        verbose_name="Attempts",
    )
    result = models.CharField(
        max_length=255,
        db_column="result",
        blank=True,
        null=True,
        help_text="Human-readable outcome (or error) written by the game.",
        verbose_name="Result",
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        blank=True,
        null=True,
        verbose_name="Created At",
    )
    processed_at = models.DateTimeField(
        db_column="processed_at",
        blank=True,
        null=True,
        verbose_name="Processed At",
    )

    class Meta:
        managed = False
        db_table = "web_admin_queue"
        ordering = ("-id",)
        verbose_name = "Web Admin Task"
        verbose_name_plural = "Web Admin Tasks"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.id})"

    def __str__(self) -> str:
        return f"{self.get_command_display()} [{self.status}]"
