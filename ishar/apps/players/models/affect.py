from django.db import models

from .player import Player
from .skill import Skill


class PlayerAffect(models.Model):
    """Ishar player affect."""
    player_affect_id = models.AutoField(
        primary_key=True,
        help_text="Primary key player affect identification number.",
        verbose_name="Player Affect ID"
    )
    player = models.ForeignKey(
        to=Player,
        on_delete=models.DO_NOTHING,
        help_text="Player related to the affect.",
        verbose_name="Player"
    )
    affect = models.ForeignKey(
        to=Skill,
        on_delete=models.DO_NOTHING,
        help_text="Skill related to the player affect.",
        verbose_name="Affect"
    )
    expires = models.IntegerField(
        help_text="Expires value for the player affect.",
        verbose_name="Expires"
    )
    bits = models.IntegerField(
        help_text='Bits number value for the player affect.',
        verbose_name="Bits"
    )
    location_1 = models.IntegerField(
        help_text='First location ("location_1") number for the player affect.',
        verbose_name="Location 1"
    )
    mod_1 = models.IntegerField(
        help_text='First mod ("mod_1") number for the player affect.',
        verbose_name="Mod 1"
    )
    location_2 = models.IntegerField(
        help_text=(
            'Second location ("location_2") number for the player affect.'
        ),
        verbose_name="Location 2"
    )
    mod_2 = models.IntegerField(
        help_text='Second mod ("mod_2") number for the player affect.',
        verbose_name="Mod 2"
    )
    aflags_blob = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Affect flags blob for the player affect.",
        verbose_name="AFlags Blob"
    )

    class Meta:
        managed = False
        db_table = "player_affects"
        ordering = ("player", "affect",)
        unique_together = (("player", "affect"),)
        verbose_name = "Player Affect"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s @ %s" % (
            self.affect,
            self.player
        )
