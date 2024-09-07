from django.db import models

from apps.players.models.player import PlayerBase

from .challenge import Challenge


class PlayerChallenge(models.Model):
    """Ishar player challenge."""
    player_challenges_id = models.AutoField(
        primary_key=True,
        help_text=(
            "Primary key identification number of player challenge relation."
        ),
        verbose_name="Player Challenges ID"
    )
    player = models.ForeignKey(
        to=PlayerBase,
        on_delete=models.DO_NOTHING,
        help_text="Player related to a challenge.",
        verbose_name="Player"
    )
    challenge = models.ForeignKey(
        to=Challenge,
        on_delete=models.DO_NOTHING,
        help_text="Challenge related to a player.",
        verbose_name="Challenge"
    )
    last_completed = models.DateTimeField(
        help_text=(
            "Date and time when the challenge was last completed by the player."
        ),
        verbose_name="Last Completed"
    )

    class Meta:
        managed = False
        db_table = "player_challenges"
        default_related_name = "player_challenges"
        unique_together = (("player", "challenge"),)
        verbose_name = "Player Challenge"
        verbose_name_plural = "Player Challenges"
