from django.contrib.admin import display
from django.db import models


class ClassManager(models.Manager):
    def get_by_natural_key(self, class_name):
        # Natural key by class name.
        return self.get(class_name=class_name)


class Class(models.Model):
    """Ishar player/mobile class."""

    objects = ClassManager()

    class_id = models.PositiveIntegerField(
        primary_key=True,
        help_text="Permanent class identification number.",
        verbose_name="Class ID",
    )
    class_name = models.CharField(
        unique=True,
        max_length=15,
        help_text="Name of the class.",
        verbose_name="Class Name",
    )
    class_display = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="Display text of the class.",
        verbose_name="Class Display",
    )
    class_description = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="Description text of the class.",
        verbose_name="Class Description",
    )
    is_playable = models.BooleanField(
        help_text="Is the class playable?",
        verbose_name="Playable?",
    )
    base_hit_pts = models.IntegerField(
        help_text="Amount of base hit points of the class.",
        verbose_name="Base Hit Points",
    )
    hit_pts_per_level = models.IntegerField(
        help_text="Amount of hit points per level of the class.",
        verbose_name="Hit Points Per Level",
    )
    attack_per_level = models.IntegerField(
        help_text="Attack per level of the class.",
        verbose_name="Attack Per Level",
    )
    spell_rate = models.IntegerField(
        help_text="Spell rate of the class.",
        verbose_name="Spell Rate",
    )
    class_stat = models.IntegerField(
        help_text="Class stat of the class.",
        verbose_name="Class Stat",
    )
    class_dc = models.IntegerField(
        help_text="Expertise (DC) of the class.",
        verbose_name="Class Expertise (DC)",
    )
    base_fortitude = models.IntegerField(
        help_text="Base fortitude of the class.",
        verbose_name="Base Fortitude",
    )
    base_resilience = models.IntegerField(
        help_text="Base resilience of the class.",
        verbose_name="Base Resilience",
    )
    base_reflex = models.IntegerField(
        help_text="Base reflex of the class.",
        verbose_name="Base Reflex",
    )
    strength_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="Strength priority of the class.",
        verbose_name="Strength Priority",
    )
    agility_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="Agility priority of the class.",
        verbose_name="Agility Priority",
    )
    endurance_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="Endurance priority of the class.",
        verbose_name="Endurance Priority",
    )
    perception_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="Perception priority of the class.",
        verbose_name="Perception Priority",
    )
    focus_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="Focus priority of the class.",
        verbose_name="Focus Priority",
    )
    willpower_priority = models.IntegerField(
        blank=True,
        null=True,
        help_text="Willpower priority of the class.",
        verbose_name="Willpower Priority",
    )

    class Meta:
        managed = False
        db_table = "classes"
        ordering = ("class_name",)
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.get_class_name()

    @display(description="Class Name", ordering="class_name")
    def get_class_name(self) -> str:
        # Formatted class name.
        return self.class_name.replace("_", " ").title()

    def natural_key(self) -> str:
        # Natural key by class name.
        return self.get_class_name()
