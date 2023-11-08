from django.contrib import admin
from django.db import models

from ishar.apps.races.models import Race
from ishar.apps.skills.models import Skill


class Class(models.Model):
    """
    Player/Mobile Class.
    """
    class_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated primary key identifying class.",
        verbose_name="Class ID"
    )
    class_name = models.CharField(
        unique=True,
        max_length=15,
        help_text="Name of the class.",
        verbose_name="Class Name"
    )
    class_display = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="Display text of the class.",
        verbose_name="Class Display"
    )
    class_description = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="Description text of the class.",
        verbose_name="Class Description"
    )
    is_playable = models.BooleanField(
        help_text="Is the class playable?",
        verbose_name="Playable?"
    )
    base_hit_pts = models.IntegerField(
        help_text="Amount of base hit points of the class.",
        verbose_name="Base Hit Points"
    )
    hit_pts_per_level = models.IntegerField(
        help_text="Amount of hit points per level of the class.",
        verbose_name="Hit Points Per Level"
    )
    attack_per_level = models.IntegerField(
        help_text="Attack per level of the class.",
        verbose_name="Attack Per Level"
    )
    spell_rate = models.IntegerField(
        help_text="Spell rate of the class.",
        verbose_name="Spell Rate"
    )
    class_stat = models.IntegerField(
        help_text="Class stat of the class.",
        verbose_name="Class Stat"
    )
    class_dc = models.IntegerField(
        help_text="Expertise (DC) of the class.",
        verbose_name="Class Expertise (DC)"
    )
    base_fortitude = models.IntegerField(
        help_text="Base fortitude of the class.",
        verbose_name="Base Fortitude"
    )
    base_resilience = models.IntegerField(
        help_text="Base resilience of the class.",
        verbose_name="Base Resilience"
    )
    base_reflex = models.IntegerField(
        help_text="Base reflex of the class.",
        verbose_name="Base Reflex")

    class Meta:
        managed = False
        db_table = "classes"
        ordering = ("class_name",)
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} [{self.class_id}]"

    def __str__(self) -> str:
        return self.get_class_name()

    @admin.display(description="Class Name", ordering="class_name")
    def get_class_name(self) -> str:
        """Formatted class name."""
        return self.class_name.replace("_", " ").title()


class ClassLevel(models.Model):
    """
    Class Level.
    """
    class_level_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated primary key for class level identifier.",
        verbose_name="Class Level ID"
    )
    level = models.IntegerField(
        help_text="Level of the class level.",
        verbose_name="Level"
    )
    male_title = models.CharField(
        max_length=80,
        help_text="Male title of the class level.",
        verbose_name="Male Title"
    )
    female_title = models.CharField(
        max_length=80,
        help_text="Female title of the class level.",
        verbose_name="Female Title"
    )
    player_class = models.ForeignKey(
        to=Class,
        db_column="class_id",
        on_delete=models.DO_NOTHING,
        help_text="Class of the class level.",
        verbose_name="Class"
    )
    experience = models.IntegerField(
        help_text="Experience of the class level.",
        verbose_name="Experience"
    )

    class Meta:
        managed = False
        db_table = "class_levels"
        ordering = ()
        verbose_name = "Class Level"
        verbose_name_plural = "Class Levels"

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}: {self.__str__()}"
                f"[{self.class_level_id}]")

    def __str__(self) -> str:
        return f"Level {self.level} @ {self.player_class}"


class ClassRace(models.Model):
    """
    Class Race.
    """
    classes_races_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated primary key for class race identifier.",
        verbose_name="Class Race ID"
    )
    race = models.ForeignKey(
        to=Race,
        db_column="race_id",
        on_delete=models.DO_NOTHING,
        help_text="Race of the class race relation.",
        verbose_name="Race"
    )
    player_class = models.ForeignKey(
        to=Class,
        db_column="class_id",
        on_delete=models.DO_NOTHING,
        help_text="Class of the class race relation.",
        verbose_name="Class"
    )

    class Meta:
        managed = False
        db_table = "classes_races"
        ordering = ("-classes_races_id",)
        verbose_name = "Class Race"
        verbose_name_plural = "Classes Races"

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}: {self.__str__()}"
                f"[{self.classes_races_id}]")

    def __str__(self) -> str:
        return f"{self.race} @ {self.player_class}"


class ClassSkill(models.Model):
    """
    Class Skill.
    """
    class_skills_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated primary key for class skill identifier.",
        verbose_name="Class Skill ID"
    )
    player_class = models.ForeignKey(
        to=Class,
        db_column="class_id",
        on_delete=models.DO_NOTHING,
        help_text="Class of the class skill.",
        verbose_name="Class"
    )
    skill = models.ForeignKey(
        to=Skill,
        db_column="skill_id",
        on_delete=models.DO_NOTHING,
        help_text="Skill of the class skill.",
        verbose_name="Skill"
    )
    min_level = models.IntegerField(
        db_column="min_level",
        help_text="Minimum level of the class skill.",
        verbose_name="Minimum Level"
    )
    max_learn = models.IntegerField(
        db_column="max_learn",
        help_text="Maximum learn of the class skill.",
        verbose_name="Maximum Learn"
    )

    class Meta:
        managed = False
        db_table = "class_skills"
        ordering = ("-class_skills_id",)
        verbose_name = "Class Skill"
        verbose_name_plural = "Class Skills"

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}: {self.__str__()} "
                f"[{self.class_skills_id}]")

    def __str__(self) -> str:
        return f"{self.skill} @ {self.player_class}"
