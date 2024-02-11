from django.db import models


class SkillMod(models.IntegerChoices):
    """
    Skill mod.
    """
    NONE = 0, "None"
    NEGATIVE_ONE = -1, "Negative One"
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


class PlayerPosition(models.IntegerChoices):
    """
    Player positions.
    """
    NEGATIVE_ONE = -1, "Negative One [-1]"
    POSITION_DEAD = 0, "Dead [0]"
    POSITION_DYING = 1, "Dying [1]"
    POSITION_STUNNED = 2, "Stunned [2]"
    POSITION_PARALYZED = 3, "Paralyzed [3]"
    POSITION_SLEEPING = 4, "Sleeping [4]"
    POSITION_HOISTED = 5, "Hoisted [5]"
    POSITION_RESTING = 6, "Resting [6]"
    POSITION_SITTING = 7, "Sitting [7]"
    POSITION_RIDING = 8, "Riding [8]"
    UNUSED_POSN = 9, "Unused [9]"
    POSITION_STANDING = 10, "Standing [10]"


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
        max_length=255,
        blank=True,
        null=True,
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
    decide_func = models.TextField(
        blank=True, null=True,
        help_text="Internal function for decision-making for the skill/spell.",
        verbose_name="Decide Function"
    )
    skill_type = models.IntegerField(
        choices=(
            (0, "Type [0]"),
            (1, "Skill [1]"),
            (2, "Spell [2]"),
            (3, "Craft [3]")
        ),
        help_text="Type of skill.",
        verbose_name="Skill Type"
    )
    parent_skill = models.IntegerField(
        default=-1,
        help_text='Parent skill ID of a skill. Value of "-1" means no parent.',
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
        ordering = ("skill_name",)
        managed = False
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.skill_name or self.enum_symbol


class SkillComponent(models.Model):
    """
    Skill Component.
    """
    skill_components_id = models.AutoField(
        blank=False,
        db_column="skill_components_id",
        editable=False,
        null=False,
        help_text="Auto-generated ID number of the skill-component relation.",
        primary_key=True,
        verbose_name="Skill Component ID"
    )
    skill = models.ForeignKey(
        blank=False,
        db_column="skill_id",
        help_text="Skill related to a component.",
        null=False,
        on_delete=models.CASCADE,
        to=Skill,
        verbose_name="Skill"
    )
    component_type = models.IntegerField(
        blank=False,
        choices=(
            (0, "None [0]"),
            (1, "Treasure [1]"),
            (2, "Item [2]")
        ),
        help_text="Type of component.",
        null=False,
        verbose_name="Component Type"
    )
    component_value = models.IntegerField(
        blank=False,
        help_text="Value of component.",
        null=False,
        verbose_name="Component Value"
    )
    component_count = models.SmallIntegerField(
        blank=False,
        default=1,
        null=False,
        help_text="Count of components.",
        verbose_name="Component Count"
    )

    class Meta:
        managed = False
        db_table = "skill_components"
        ordering = ("skill_components_id", "skill")
        verbose_name = "Skill Component"
        verbose_name_plural = "Skill Components"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}: {self.__str__()} @ "
            f"[{self.skill_components_id}]"
        )

    def __str__(self):
        return (
            f"{self.skill} / {self.get_component_type_display()}: "
            f"{self.component_value}"
        )


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
        return f"{self.__class__.__name__}: {self.__str__()} [{self.id}]"

    def __str__(self):
        return f"{self.skill} @ {self.force}"


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
