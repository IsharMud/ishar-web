"""Site-owned per-account map state for the web HUD (isharmud/ishar-web#125).

Unlike most models in this repo, these two tables are **owned by the site**
(``managed = True`` — migrations live here, the game never touches them),
following the same shared-database pattern as ``web_login_token``: rows key
on ``account_id`` as a plain integer rather than a cross-ownership FK into
the game's ``accounts`` table.

* ``RoomDiscovery`` — fog-of-war: one row per (account, room) ever seen.
  The zone graph itself is served from the game's authoritative ``rooms`` /
  ``room_exits`` tables; discovery only controls what the client *reveals*.
* ``RoomNote`` — a player's personal note on a room, shown on the map and
  in the Room panel.

``zone_id`` is denormalized onto both so per-zone state loads with one
indexed query; it is always resolved server-side from the posted vnums
(never trusted from the client).
"""
from django.db import models

from apps.core.models.unsigned import UnsignedAutoField


class RoomDiscovery(models.Model):
    """One (account, room) fog-of-war fact."""

    id = UnsignedAutoField(primary_key=True)
    account_id = models.IntegerField(
        db_index=True,
        help_text="Account that discovered the room.",
        verbose_name="Account ID",
    )
    room_vnum = models.IntegerField(
        help_text="VNUM of the discovered room.",
        verbose_name="Room VNUM",
    )
    zone_id = models.IntegerField(
        help_text="Zone of the room (denormalized, resolved server-side).",
        verbose_name="Zone ID",
    )
    first_seen = models.DateTimeField(
        auto_now_add=True,
        help_text="When the account first saw the room.",
        verbose_name="First Seen",
    )

    class Meta:
        managed = True
        db_table = "web_room_discovery"
        constraints = (
            models.UniqueConstraint(
                fields=("account_id", "room_vnum"),
                name="uniq_account_room",
            ),
        )
        indexes = (models.Index(fields=("account_id", "zone_id")),)
        verbose_name = "Room Discovery"
        verbose_name_plural = "Room Discoveries"

    def __str__(self) -> str:
        return f"Account {self.account_id} discovered room {self.room_vnum}"


class RoomNote(models.Model):
    """A player's personal note on a room."""

    id = UnsignedAutoField(primary_key=True)
    account_id = models.IntegerField(
        db_index=True,
        help_text="Account the note belongs to.",
        verbose_name="Account ID",
    )
    room_vnum = models.IntegerField(
        help_text="VNUM of the room the note is about.",
        verbose_name="Room VNUM",
    )
    zone_id = models.IntegerField(
        help_text="Zone of the room (denormalized, resolved server-side).",
        verbose_name="Zone ID",
    )
    text = models.TextField(
        help_text="Note text (capped at 2000 characters by the view).",
        verbose_name="Text",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the note was created.",
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the note was last edited.",
        verbose_name="Updated At",
    )

    class Meta:
        managed = True
        db_table = "web_room_note"
        constraints = (
            models.UniqueConstraint(
                fields=("account_id", "room_vnum"),
                name="uniq_account_room_note",
            ),
        )
        indexes = (models.Index(fields=("account_id", "zone_id")),)
        verbose_name = "Room Note"
        verbose_name_plural = "Room Notes"

    def __str__(self) -> str:
        return f"Account {self.account_id} note on room {self.room_vnum}"
