from django.db import models
from django.utils.translation import gettext_lazy as _

from ishar.apps.players.models.player import Player
from ishar.apps.players.models.remort_upgrade import RemortUpgrade


class PlayerRemortUpgrade(models.Model):
    """
    Player relation to a remort upgrade.
    """
    player = models.ForeignKey(
        # primary_key=True,  # Fake it, just so reads work.
        db_column="player_id",
        editable=False,
        related_query_name="remort_upgrade",
        related_name="all_remort_upgrades",
        to=Player,
        to_field="id",
        on_delete=models.DO_NOTHING,
        help_text="Player with a remort upgrade.",
        verbose_name="Player"
    )
    upgrade = models.OneToOneField(
        db_column="upgrade_id",
        editable=False,
        to=RemortUpgrade,
        to_field="upgrade_id",
        primary_key=True,
        related_query_name="+",
        on_delete=models.DO_NOTHING,
        help_text="Remort upgrade affecting a player.",
        verbose_name="Remort Upgrade"
    )
    value = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False,
        help_text="Value of a player's remort upgrade.",
        verbose_name="Value"
    )
    essence_perk = models.BooleanField(
        help_text="Is the player's remort upgrade an essence perk?",
        verbose_name="Essence Perk?"
    )

    class Meta:
        managed = False
        db_table = "player_remort_upgrades"
        ordering = ("upgrade", "player")
        unique_together = (("upgrade", "player"),)
        verbose_name = _("Player's Remort Upgrade")
        verbose_name_plural = _("Player's Remort Upgrades")

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return "%s @ %s" % (
            self.upgrade,
            self.player
        )
