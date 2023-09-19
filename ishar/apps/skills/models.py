from django.db import models
from django.conf import settings


class Force(models.Model):
    """
    Force.
    """
    force_name = models.CharField(
        unique=True,
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of the force.",
        verbose_name="Force Name"
    )

    class Meta:
        managed = False
        db_table = "forces"
        ordering = ("force_name",)
        verbose_name = "Force"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.force_name


class SpellFlag(models.Model):
    """
    Spell Flag.
    """
    id = models.AutoField(
        blank=False,
        editable=False,
        help_text=(
            "Auto-generated permanent identification number for a spell flag."
        ),
        null=False,
        primary_key=True,
        verbose_name="Spell Flag ID"
    )
    name = models.CharField(
        max_length=50,
        help_text="Name of the spell flag.",
        verbose_name="Spell Flag Name"
    )
    description = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Description of the spell flag.",
        verbose_name="Spell Flag Description"
    )

    class Meta:
        db_table = "spell_flags"
        managed = False
        ordering = ("name",)
        verbose_name = "Flag"

    def __repr__(self):
        return f"{self.__class__.__name__} : {repr(self.__str__())} ({self.id})"

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Skill (includes spells).
    """
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
        max_length=255, blank=True, null=True,
        help_text="Internal function name for the skill/spell.",
        verbose_name="Function Name"
    )
    skill_name = models.TextField(
        blank=True, null=True,
        help_text="Friendly name of the skill/spell.",
        verbose_name="Skill Name"
    )
    min_posn = models.IntegerField(
        blank=True,
        choices=settings.PLAYER_POSITIONS,
        null=True,
        help_text="Minimum position to use the skill/spell.",
        verbose_name="Minimum Position"
    )
    min_use = models.IntegerField(
        blank=True, null=True,
        help_text="Minimum use of the skill/spell.",
        verbose_name="Minimum Use"
    )
    spell_breakpoint = models.IntegerField(
        blank=True, null=True,
        help_text="Breakpoint of the skill/spell.",
        verbose_name="Spell Breakpoint"
    )
    held_cost = models.IntegerField(
        blank=True, null=True,
        help_text="Held cost of the skill/spell.",
        verbose_name="Held Cost"
    )
    wearoff_msg = models.TextField(
        blank=True, null=True,
        help_text="Message shown to the user when skill/spell wears off.",
        verbose_name="Wear-Off Message"
    )
    chant_text = models.TextField(
        blank=True, null=True,
        help_text="Text chanted to use the skill/spell.",
        verbose_name="Chant Text"
    )
    difficulty = models.IntegerField(
        blank=True, null=True,
        help_text="Difficulty of the skill/spell.",
        verbose_name="Difficulty"
    )
    rate = models.IntegerField(
        blank=True, null=True,
        help_text="Rate of the skill/spell.",
        verbose_name="Rate"
    )
    notice_chance = models.IntegerField(
        blank=True, null=True,
        help_text="Notice chance of the skill/spell.",
        verbose_name="Notice Chance"
    )
    appearance = models.TextField(
        blank=True, null=True,
        help_text="Appearance of the skill/spell.",
        verbose_name="Appearance"
    )
    component_type = models.IntegerField(
        blank=True, null=True,
        help_text="Component type of the skill/spell.",
        verbose_name="Component Type"
    )
    component_value = models.IntegerField(
        blank=True, null=True,
        help_text="Component value of the skill.",
        verbose_name="Component Value"
    )
    scale = models.IntegerField(
        blank=True, null=True,
        help_text="Scale of the skill/spell.",
        verbose_name="Scale"
    )
    mod_stat_1 = models.IntegerField(
        blank=True, null=True,
        help_text="Mod stat 1 of the skill/spell.",
        verbose_name="Mod Stat 1"
    )
    mod_stat_2 = models.IntegerField(
        blank=True, null=True,
        help_text="Mod stat 2 of the skill/spell.",
        verbose_name="Mod Stat 2"
    )
    is_spell = models.BooleanField(
        help_text="Is this a spell?",
        verbose_name="Is Spell?"
    )
    is_skill = models.BooleanField(
        help_text="Is this a skill?",
        verbose_name="Is Skill?"
    )
    is_type = models.BooleanField(
        help_text="Is this a type?",
        verbose_name="Is Type?"
    )
    decide_func = models.TextField(
        blank=True, null=True,
        help_text="Internal function for decision-making for the skill/spell.",
        verbose_name="Decide Function"
    )

    class Meta:
        db_table = "skills"
        ordering = (
            "-is_spell", "-is_skill", "-is_type", "skill_name", "enum_symbol"
        )
        managed = False
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.skill_name or self.enum_symbol


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
        verbose_name="ID"
    )
    skill = models.ForeignKey(
        db_column="skill_id",
        to=Skill,
        on_delete=models.CASCADE,
        help_text="Skill/spell related to a force.",
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

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.skill)} @ {self.force}"

    def __str__(self):
        return self.__repr__()


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
