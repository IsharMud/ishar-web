"""Live presence, published by the game (isharmud/ishar-mud#1771).

These two tables are the game's authoritative "who is online" signal, written
by the engine's presence heartbeat (`rust-interop/src/presence.rs`) and read
here — the contract is `ishar-mud/docs/web_bridge_contracts.md` (Contract 2).
Both are ``managed = False``: the game owns the schema.

Why they exist: the site used to infer online state from ``logon >= logout``,
which breaks both ways — the game's 5-minute autosave rewrites ``logout`` mid
session (online players vanish) and a crash freezes ``logon >= logout`` forever
(ghosts persist). The engine now publishes presence directly:

* ``game_presence`` — one row per character currently in the PLAYING state.
  Rows are added on enter, removed on leave/socket teardown, and their
  ``last_seen`` is refreshed every game-minute. A row older than
  ``PRESENCE_STALE_SECONDS`` (two missed pulses) means the game died without
  cleanup — treat it as offline.
* ``game_status`` — a singleton (id always 1) carrying the boot time, the last
  heartbeat, and the live player count. Its existence is what distinguishes
  "game up, zero players" (row present, no presence rows) from "game never
  integrated / down pre-rollout" (row absent) — a presence-rows-only design
  cannot tell those apart.
"""
from django.db import models


# A presence row (or heartbeat) older than this is stale: the game refreshes
# every game-minute (~60s), so two missed pulses ⇒ the writer is gone. Matches
# the reader rule in the bridge contract.
PRESENCE_STALE_SECONDS = 120

# The game_status singleton always lives at id = 1.
GAME_STATUS_ID = 1


class GamePresence(models.Model):
    """One row per character currently in the game (PLAYING state)."""

    player_id = models.PositiveIntegerField(
        primary_key=True,
        db_column="player_id",
        help_text="players.id of the character in-game.",
        verbose_name="Player ID",
    )
    account_id = models.IntegerField(
        db_column="account_id",
        help_text="Owning account id.",
        verbose_name="Account ID",
    )
    name = models.CharField(
        max_length=20,
        help_text="Character name.",
        verbose_name="Name",
    )
    logged_in_at = models.DateTimeField(
        help_text="When the character entered the game.",
        verbose_name="Logged In At",
    )
    last_seen = models.DateTimeField(
        help_text="Last presence pulse for the character.",
        verbose_name="Last Seen",
    )
    is_immortal = models.BooleanField(
        default=False,
        help_text="Whether the character is an immortal.",
        verbose_name="Is Immortal?",
    )

    class Meta:
        managed = False
        db_table = "game_presence"
        ordering = ("logged_in_at",)
        verbose_name = "Game Presence"
        verbose_name_plural = "Game Presence"

    def __str__(self) -> str:
        return self.name


class GameStatus(models.Model):
    """Singleton heartbeat for the whole game process (id always 1)."""

    id = models.PositiveSmallIntegerField(
        primary_key=True,
        help_text="Always 1 — this is a singleton.",
        verbose_name="ID",
    )
    booted_at = models.DateTimeField(
        help_text="When the game process last booted.",
        verbose_name="Booted At",
    )
    heartbeat_at = models.DateTimeField(
        help_text="Timestamp of the most recent presence pulse.",
        verbose_name="Heartbeat At",
    )
    player_count = models.IntegerField(
        default=0,
        help_text="Number of characters in-game at the last pulse.",
        verbose_name="Player Count",
    )

    class Meta:
        managed = False
        db_table = "game_status"
        verbose_name = "Game Status"
        verbose_name_plural = "Game Status"

    def __str__(self) -> str:
        return f"Game status (heartbeat {self.heartbeat_at})"
