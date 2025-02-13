from django.db import models

from apps.core.models.player_flag import PlayerFlag

from .player import PlayerBase


class PlayerPlayerFlag(models.Model):
    """Ishar player flag."""

    flag = models.OneToOneField(
        primary_key=True,
        to=PlayerFlag,
        on_delete=models.DO_NOTHING,
        editable=False,
        related_query_name="+",
        help_text="Flag affecting a player.",
        verbose_name="Flag",
    )
    player = models.ForeignKey(
        to=PlayerBase,
        on_delete=models.DO_NOTHING,
        editable=False,
        related_name="flag",
        related_query_name="flags",
        help_text="Player affected by a flag.",
        verbose_name="Player",
    )
    value = models.BooleanField(
        editable=False,
        help_text="Value of the flag affecting the player.",
        verbose_name="Value",
    )

    class Meta:
        managed = False
        db_table = "player_player_flags"
        # The composite primary key (flag_id, player_id) found,
        #   that is not supported. The first column is selected.
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("flag", "player",),
                name="pflag_per_player",
            ),
        )
        unique_together = (("flag", "player",),)
        ordering = (
            "player",
            "flag",
            "-value"
        )
        verbose_name = "Player's Flag"
        verbose_name_plural = "Player's Flags"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return f"{self.flag} @ {self.player}"
