from django.db import models

from .skill import Skill


class SkillModType(models.IntegerChoices):
    """
    Skill mod types.
    """
    NONE = 0, "None"
    STRENGTH = 1, "Strength"
    PERCEPTION = 2, "Perception"
    FOCUS = 3, "Focus"
    AGILITY = 4, "Agility"
    ENDURANCE = 5, "Endurance"
    WILLPOWER = 6, "Willpower"
    SPEED = 7, "Speed"
    SEX = 8, "Sex"
    AGE = 9, "Age"
    WEIGHT = 10, "Weight"
    HEIGHT = 11, "Height"
    SPELL_POINTS = 12, "Spell Points"
    HIT_POINTS = 13, "Hit Points"
    MOVE_POINTS = 14, "Move Points"
    ARMOR = 15, "Armor"
    ATTACK = 16, "Attack"
    DAMAGE = 17, "Melee Damage"
    HEAL = 18, "Heal"
    SAVE_POISON = 19, "Fortitude"
    SAVE_PETRIFICATION = 20, "Fortitude"
    SAVE_BREATH = 21, "Reflex"
    SAVE_MAGIC = 22, "Resilience"
    ALIGNMENT = 23, "Alignment"
    LIGHT_IN = 24, "Light In"
    LIGHT_ON = 25, "Light On"
    FIRESHIELD = 26, "Fireshield"
    SAVE_ILLUSION = 27, "Resilience"
    HEAL_HIT = 28, "Heal Hit"
    HEAL_SPELL = 29, "Heal Spell"
    HEAL_MOVE = 30, "Heal Move"
    HEAL_FAVOR = 31, "Heal Favor"
    SAVE_ALL = 32, "Save All"
    CRITICAL = 33, "Critical"
    BODY = 34, "Body"
    MIND = 35, "Mind"
    XP = 36, "Experience"
    SAVE_DISTRACTION = 37, "Resilience"
    SUSTAIN_SPELL = 38, "Sustained Spell"
    EXPERTISE = 39, "Expertise"
    SAVE_FORTITUDE = 40, "Fortitude"
    SAVE_REFLEX = 41, "Reflex"
    SAVE_RESILIENCE = 42, "Resilience"
    SPELL_POTENCY = 43, "Spell Potency"
    RESISTANCE = 44, "Resistance"
    SPELL_DAMAGE = 45, "Spell Damage"
    HEALING_POWER = 46, "Healing Power"
    SUSCEPTIBILITY = 47, "Susceptibility"
    IMMUNITY = 48, "Immunity"
    VULNERABILITY = 49, "Vulnerability"


class SkillMod(models.Model):
    """
    Skill mod.
    """
    skill_mod_id = models.AutoField(
        primary_key=True,
        help_text = "Auto-generated permanent unique skill mod number.",
        verbose_name="Skill Mod ID"
    )
    skill = models.ForeignKey(
        db_column="skill_id",
        to=Skill,
        on_delete=models.CASCADE,
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
        return f"{self.__class__.__name__}: {self.__str__()} [{self.pk}]"

    def __str__(self):
        return f"{self.get_mod_location_display()} @ {self.skill}"
