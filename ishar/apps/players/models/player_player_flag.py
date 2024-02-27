from django.db import models

from ishar.apps.players.models.flag import PlayerFlag
from ishar.apps.players.models.player import Player


class PlayerPlayerFlag(models.Model):
    """
    Player's Flag.
    """
    flag = models.OneToOneField(
        primary_key=True,
        to=PlayerFlag,
        on_delete=models.CASCADE,
        editable=False,
        related_query_name="+",
        help_text="Flag affecting a player.",
        verbose_name="Flag"
    )
    player = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        editable=False,
        related_name="flag",
        related_query_name="flags",
        help_text="Player affected by a flag.",
        verbose_name="Player"
    )
    value = models.BooleanField(
        editable=False,
        help_text="Value of the flag affecting the player.",
        verbose_name="Value"
    )

    class Meta:
        managed = False
        db_table = "player_player_flags"
        # The composite primary key (flag_id, player_id) found,
        #   that is not supported. The first column is selected.
        unique_together = (("flag", "player"),)
        ordering = ("player", "flag", "-value")
        verbose_name = "Player's Flag"
        verbose_name_plural = "Player's Flags"

    def __repr__(self) -> str:
        return "%s: %s (%s)" % (
            self.__class__.__name__, self.__str__(), self.value
        )

    def __str__(self) -> str:
        return "%s @ %s" % (self.flag, self.player)
