from django.db import models

from .quest import Quest


class PlayerQuest(models.Model):
    """A player's per-quest state (`player_quests`), written by the game."""

    pk = models.CompositePrimaryKey("quest_id", "player_id")
    quest = models.ForeignKey(
        to=Quest,
        on_delete=models.DO_NOTHING,
        related_name="player_quests",
        related_query_name="player_quest",
        help_text="Quest which the player has interacted with.",
        verbose_name="Quest",
    )
    player = models.ForeignKey(
        to="players.Player",
        on_delete=models.DO_NOTHING,
        related_name="quests",
        related_query_name="quest",
        help_text="Player character undertaking the quest.",
        verbose_name="Player",
    )
    status = models.SmallIntegerField(
        help_text="Game-side status of the quest for the player.",
        verbose_name="Status",
    )
    last_completed_at = models.DateTimeField(
        help_text="Date and time the player last completed the quest.",
        verbose_name="Last Completed At",
    )
    num_completed = models.SmallIntegerField(
        help_text="Number of times the player has completed the quest.",
        verbose_name="Number Completed",
    )

    class Meta:
        managed = False
        db_table = "player_quests"
        ordering = ("-last_completed_at",)
        verbose_name = "Player Quest"
        verbose_name_plural = "Player Quests"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return f"{self.quest} @ {self.player}"
