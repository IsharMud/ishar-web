"""Site-owned per-account quest tracking for the web HUD
(isharmud/ishar-web#150).

Same shared-database pattern as the map state (``models/map.py``): the
table is **owned by the site** (``managed = True``), keyed on
``account_id`` as a plain integer. Tracking is a HUD presentation
preference — which quests pin to the top of the Quest Log and appear in
the objectives tracker — synced across the account's devices; the game
never reads it.
"""
from django.db import models

from apps.core.models.unsigned import UnsignedAutoField


class QuestTrack(models.Model):
    """One (account, quest) tracked-quest fact."""

    id = UnsignedAutoField(primary_key=True)
    account_id = models.IntegerField(
        db_index=True,
        help_text="Account tracking the quest.",
        verbose_name="Account ID",
    )
    quest_id = models.IntegerField(
        help_text="Quest ID being tracked (game quests table key).",
        verbose_name="Quest ID",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the quest was tracked.",
        verbose_name="Created At",
    )

    class Meta:
        managed = True
        db_table = "web_quest_track"
        constraints = (
            models.UniqueConstraint(
                fields=("account_id", "quest_id"),
                name="uniq_account_quest_track",
            ),
        )
        verbose_name = "Quest Track"
        verbose_name_plural = "Quest Tracks"

    def __str__(self) -> str:
        return f"Account {self.account_id} tracks quest {self.quest_id}"
