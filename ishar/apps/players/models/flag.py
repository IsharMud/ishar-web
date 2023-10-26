from django.db import models

from ishar.apps.players.models import Player


class PlayerFlag(models.Model):
    """
    Player Flag.
    """
    flag_id = models.AutoField(
        db_column="flag_id",
        primary_key=True,
        help_text="Auto-generated permanent player flag identification number.",
        verbose_name="Player Flag ID"
    )
    name = models.CharField(
        blank=False,
        db_column="name",
        max_length=20,
        null=False,
        help_text="Name of the player flag.",
        unique=True,
        verbose_name="Player Flag Name"
    )

    class Meta:
        managed = False
        db_table = "player_flags"
        ordering = ("name", "flag_id")
        verbose_name = "Flag"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())} ({self.flag_id})"
        )

    def __str__(self) -> str:
        return self.name


class PlayersFlag(models.Model):
    """
    Player's Flag.
    """
    flag = models.ForeignKey(
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
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())}"
        )

    def __str__(self) -> str:
        return f"{self.flag} @ {self.player} : {self.value}"
