from django.db import models

from .force import Force
from .skill import Skill


class SkillForce(models.Model):
    """
    Skill Force.
    """
    id = models.AutoField(
        blank=False,
        db_column="id",
        editable=False,
        null=False,
        help_text="Auto-generated ID number of the skill-force relation.",
        primary_key=True,
        verbose_name="Skill Force ID"
    )
    skill = models.ForeignKey(
        db_column="skill_id",
        to=Skill,
        on_delete=models.CASCADE,
        help_text="Skill/spell related to a force.",
        related_name="forces",
        related_query_name="force",
        verbose_name="Skill"
    )
    force = models.ForeignKey(
        db_column="force_id",
        to=Force,
        on_delete=models.CASCADE,
        help_text="Force related to a skill/spell.",
        verbose_name="Force"
    )

    class Meta:
        managed = False
        db_table = "skill_forces"
        ordering = ("id", "skill", "force")
        verbose_name = "Skill Force"
        verbose_name_plural = "Skill Forces"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s @ %s" % (self.skill, self.force)
