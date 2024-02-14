from django.db import models

from .skill import Skill


class SkillModType(models.IntegerChoices):
    """
    Skill mod types.
    """
    NEGATIVE_ONE = -1
    NONE = 0
    STRENGTH = 1
    PERCEPTION = 2
    FOCUS = 3
    AGILITY = 4
    ENDURANCE = 5
    WILLPOWER = 6
    SPEED = 7
    SEX = 8
    AGE = 9
    WEIGHT = 10
    HEIGHT = 11
    SPELL_POINTS = 12
    HIT_POINTS = 13
    MOVE_POINTS = 14
    ARMOR = 15
    ATTACK = 16
    MELEE_DAMAGE = 17
    HEAL = 18
    SAVE_POISON = 19
    SAVE_PETRIFICATION = 20
    SAVE_BREATH = 21
    SAVE_MAGIC = 22
    ALIGNMENT = 23
    LIGHT_IN = 24
    LIGHT_ON = 25
    FIRESHIELD = 26
    SAVE_ILLUSION = 27
    HEAL_HIT = 28
    HEAL_SPELL = 29
    HEAL_MOVE = 30
    HEAL_FAVOR = 31
    SAVE_ALL = 32
    CRITICAL = 33
    BODY = 34
    MIND = 35
    EXPERIENCE = 36
    SAVE_DISTRACTION = 37
    SUSTAINED_SPELL = 38
    EXPERTISE = 39
    SAVE_FORTITUDE = 40
    SAVE_REFLEX = 41
    SAVE_RESILIENCE = 42
    SPELL_POTENCY = 43
    RESISTANCE = 44
    SPELL_DAMAGE = 45
    HEALING_POWER = 46
    SUSCEPTIBILITY = 47
    IMMUNITY = 48
    VULNERABILITY = 49


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
        return "%s: %s (%i)" %(
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return "%s @ %s" % (self.get_mod_location_display(), self.skill)
