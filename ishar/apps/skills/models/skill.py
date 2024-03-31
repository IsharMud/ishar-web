from django.db import models

from .type.position import PlayerPosition
from .type.type import SkillType


class SkillManager(models.Manager):
    def get_by_natural_key(self, skill_name):
        return self.get(skill_name=skill_name)


class Skill(models.Model):
    """Ishar skill/spell."""
    id = models.AutoField(
        blank=False,
        db_column="id",
        editable=False,
        null=False,
        help_text="Auto-generated permanent ID number of the skill/spell.",
        primary_key=True,
        verbose_name="ID"
    )
    enum_symbol = models.CharField(
        max_length=255,
        help_text="Internal ENUM symbol of the skill/spell.",
        verbose_name="ENUM Symbol"
    )
    func_name = models.CharField(
        blank=True,
        max_length=255,
        null=True,
        help_text="Internal function name for the skill/spell.",
        verbose_name="Function Name"
    )
    skill_name = models.TextField(
        blank=True,
        help_text="Friendly name of the skill/spell.",
        null=True,
        verbose_name="Skill Name"
    )
    min_posn = models.IntegerField(
        blank=True,
        choices=PlayerPosition,
        null=True,
        help_text="Minimum position to use the skill/spell.",
        verbose_name="Minimum Position"
    )
    min_use = models.IntegerField(
        blank=True,
        null=True,
        help_text="Minimum use of the skill/spell.",
        verbose_name="Minimum Use"
    )
    spell_breakpoint = models.IntegerField(
        blank=True,
        null=True,
        help_text="Breakpoint of the skill/spell.",
        verbose_name="Spell Breakpoint"
    )
    held_cost = models.IntegerField(
        blank=True,
        null=True,
        help_text="Held cost of the skill/spell.",
        verbose_name="Held Cost"
    )
    wearoff_msg = models.TextField(
        blank=True,
        null=True,
        help_text="Message shown to the user when skill/spell wears off.",
        verbose_name="Wear-Off Message"
    )
    chant_text = models.TextField(
        blank=True,
        null=True,
        help_text="Text chanted to use the skill/spell.",
        verbose_name="Chant Text"
    )
    difficulty = models.IntegerField(
        blank=True,
        null=True,
        help_text="Difficulty of the skill/spell.",
        verbose_name="Difficulty"
    )
    rate = models.IntegerField(
        blank=True,
        null=True,
        help_text="Rate of the skill/spell.",
        verbose_name="Rate"
    )
    notice_chance = models.IntegerField(
        blank=True,
        null=True,
        help_text="Notice chance of the skill/spell.",
        verbose_name="Notice Chance"
    )
    appearance = models.TextField(
        blank=True,
        null=True,
        help_text="Appearance of the skill/spell.",
        verbose_name="Appearance"
    )
    scale = models.IntegerField(
        blank=True,
        null=True,
        help_text="Scale of the skill/spell.",
        verbose_name="Scale"
    )
    mod_stat_1 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Mod stat 1 of the skill/spell.",
        verbose_name="Mod Stat 1"
    )
    mod_stat_2 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Mod stat 2 of the skill/spell.",
        verbose_name="Mod Stat 2"
    )
    decide_func = models.TextField(
        blank=True,
        null=True,
        help_text="Internal function for decision-making for the skill/spell.",
        verbose_name="Decide Function"
    )
    skill_type = models.IntegerField(
        choices=SkillType,
        help_text="Type of skill.",
        verbose_name="Skill Type"
    )
    parent_skill = models.ForeignKey(
        db_column="parent_skill",
        to="self",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=-1,
        help_text='Parent skill of skill.',
        verbose_name="Parent Skill"
    )
    special_int = models.IntegerField(
        blank=True,
        default=-1,
        null=True,
        help_text="Integer that is special.",
        verbose_name="Special Integer"
    )
    obj_display = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="Display text for object.",
        verbose_name="Object Display"
    )

    class Meta:
        db_table = "skills"
        default_related_name = "skill"
        ordering = ("skill_name",)
        managed = False
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return self.skill_name or self.enum_symbol

    def natural_key(self) -> str:
        return self.skill_name
