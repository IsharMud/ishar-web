from django.db import models

from .skill import Skill
from .flag import SpellFlag


class SkillSpellFlag(models.Model):
    """
    Skill association to a spell flag.
    """
    id = models.AutoField(
        blank=False,
        editable=False,
        null=False,
        help_text="Auto-generated ID number of the skill-flag relation.",
        primary_key=True,
        verbose_name="ID"
    )
    skill = models.ForeignKey(
        to=Skill,
        on_delete=models.CASCADE,
        db_column="skill_id",
        help_text="Skill/spell affected by the flag.",
        related_name="flags",
        related_query_name="flag",
        verbose_name="Skill"
    )
    flag = models.ForeignKey(
        to=SpellFlag,
        on_delete=models.CASCADE,
        db_column="flag_id",
        help_text="Flag affecting the skill/spell.",
        verbose_name="Flag"
    )

    class Meta:
        managed = False
        db_table = "skills_spell_flags"
        ordering = ("id", "skill", "flag")
        unique_together = (("skill", "flag"),)
        verbose_name = "Skill Flag"
        verbose_name_plural = "Skill Flags"

    def __repr__(self):
        return f"{self.__class__.__name__} : {self.__str__()} [{self.id}]"

    def __str__(self):
        return f"{self.skill} @ {self.flag}"
