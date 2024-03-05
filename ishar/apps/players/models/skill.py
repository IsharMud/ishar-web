from django.db import models

from ishar.apps.players.models.player import Player
from ishar.apps.skills.models.skill import Skill


class PlayerSkill(models.Model):
    """
    Player Skill.
    """
    skill = models.ForeignKey(
        db_column="skill_id",
        related_query_name="+",
        to=Skill,
        to_field="id",
        on_delete=models.DO_NOTHING,
        help_text="Skill/spell related to a player.",
        verbose_name="Skill"
    )
    player = models.ForeignKey(
        db_column="player_id",
        related_query_name="skill",
        related_name="skills",
        to=Player,
        to_field="id",
        on_delete=models.DO_NOTHING,
        help_text="Player with a skill/spell.",
        verbose_name="Player"
    )
    skill_level = models.PositiveIntegerField(
        help_text="Skill level of the player's skill.",
        verbose_name="Skill Level"
    )

    class Meta:
        managed = False
        db_table = "player_skills"
        # The composite primary key (skill_id, player_id) found,
        #   that is not supported. The first column is selected.
        unique_together = (("skill", "player"),)
        ordering = ("player", "skill", "skill_level")
        verbose_name = "Player Skill"
        verbose_name_plural = "Player Skills"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.pk
        )

    def __str__(self) -> str:
        return "%s @ %s" % (self.skill, self.player)
