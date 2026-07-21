"""Site-owned per-character action-bar settings for the web HUD
(isharmud/ishar-web#167).

The HUD's action bar — a player's favorite skills and pinned consumables,
in ordered numbered slots — used to live only in browser localStorage. That
made it a property of the *device*: shared across every character played on
it, and awkward to switch between. This table moves the bar server-side,
one row per character, so it follows the character across devices instead.

Same shared-database pattern as the map state and quest tracking
(``models/map.py``, ``models/quest.py``): the table is **owned by the
site** (``managed = True`` — migrations live here, the game never touches
it). It keys on the game's ``players.id`` (resolved server-side from the
connected character's GMCP name, scoped to the owning account) with
``account_id`` denormalized for ownership scoping and admin filtering.
"""
from django.db import models

from apps.core.models.unsigned import UnsignedAutoField


class HudBar(models.Model):
    """One character's action-bar slot assignments."""

    id = UnsignedAutoField(primary_key=True)
    player_id = models.IntegerField(
        unique=True,
        help_text="players.id of the character the bar belongs to.",
        verbose_name="Player ID",
    )
    account_id = models.IntegerField(
        db_index=True,
        help_text="Owning account id (denormalized for ownership scoping).",
        verbose_name="Account ID",
    )
    slots = models.JSONField(
        default=list,
        help_text=(
            "Ordered action-bar slots: skill keys (strings), pinned-item "
            "objects, or null for an empty slot. Sanitized server-side."
        ),
        verbose_name="Slots",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the bar was last saved.",
        verbose_name="Updated At",
    )

    class Meta:
        managed = True
        db_table = "web_hud_bar"
        verbose_name = "HUD Bar"
        verbose_name_plural = "HUD Bars"

    def __str__(self) -> str:
        return f"Action bar for player {self.player_id}"
