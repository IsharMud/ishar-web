from django.db import models

from ishar.apps.skills.models.skill import Skill

from .race import Race


class RaceSkill(models.Model):
    """
    Race Skill.
    """
    race_skill_id = models.AutoField(
        blank=False,
        db_column="race_skill_id",
        help_text="Primary identification number of the race skill.",
        null=False,
        primary_key=True,
        verbose_name="Race Skill ID"
    )
    race = models.ForeignKey(
        db_column="race_id",
        to=Race,
        on_delete=models.CASCADE,
        help_text="Race related to a skill.",
        related_name="skills",
        related_query_name="skill",
        verbose_name="Race"
    )
    skill = models.ForeignKey(
        db_column="skill_id",
        to=Skill,
        on_delete=models.CASCADE,
        help_text="Skill (or spell) related to a race.",
        verbose_name="Skill"
    )
    level = models.IntegerField(
        db_column="level",
        help_text="Level of a skill related to a race.",
        verbose_name="Skill Level"
    )

    class Meta:
        managed = False
        db_table = "races_skills"
        ordering = ("race", "skill", "level")
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __repr__(self):
        return "%s: %s (%s)" % (
            self.__class__.__name__, self.__str__(), self.pk
        )

    def __str__(self):
        return "%s @ %s / Level: %i" % (
            self.skill, self.race, self.level
        )
