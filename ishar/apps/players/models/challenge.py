from django.db import models
from django.utils.translation import gettext_lazy as _

from ishar.apps.challenges.models.challenge import Challenge

from .player import PlayerBase


class PlayerChallenge(models.Model):
    """Ishar player challenge."""
    player_challenges_id = models.AutoField(
        primary_key=True,
        help_text=_(
            "Primary key identification number of the player challenge."
        ),
        verbose_name=_("Player Challenges ID")
    )
    player = models.ForeignKey(
        to=PlayerBase,
        on_delete=models.DO_NOTHING,
        help_text=_("Player related to a challenge."),
        verbose_name=_("Player")
    )
    challenge = models.ForeignKey(
        to=Challenge,
        on_delete=models.DO_NOTHING,
        help_text=_("Challenge related to a player."),
        verbose_name=_("Challenge")
    )
    last_completed = models.DateTimeField(
        help_text=_(
            "Date and time that the challenge was last completed by the player."
        ),
        verbose_name=_("Last Completed")
    )

    class Meta:
        managed = False
        db_table = "player_challenges"
        unique_together = (("player", "challenge"),)
        verbose_name = "Player Challenge"
        verbose_name_plural = "Player Challenges"
