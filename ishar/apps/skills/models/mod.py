from django.db import models

from .skill import Skill
from .type.mod import SkillModType


class SkillMod(models.Model):
    """
    Ishar skill mod.
    """
    skill_mod_id = models.AutoField(
        primary_key=True,
        help_text = "Auto-generated permanent unique skill mod number.",
        verbose_name="Skill Mod ID"
    )
    skill = models.ForeignKey(
        db_column="skill_id",
        to=Skill,
        on_delete=models.DO_NOTHING,
        help_text="Skill/spell related to the mod.",
        related_name="mods",
        related_query_name="mod",
        verbose_name="Skill"
    )
    mod_location = models.SmallIntegerField(
        blank=True,
        choices=SkillModType,
        null=True,
        help_text="Location of the skill mod.",
        verbose_name="Location"
    )
    mod_value = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Value of the skill mod.",
        verbose_name="Value"
    )

    class Meta:
        managed = False
        db_table = "skill_mods"
        ordering = ("mod_location",)
        verbose_name = "Skill Mod"
        verbose_name_plural = "Skill Mod"

    def __repr__(self):
        return "%s: %s (%i)" %(
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return "%s @ %s" % (
            self.get_mod_location_display(),
            self.skill
        )
