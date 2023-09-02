from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator

from ishar.util.player import get_class_options


class Quest(models.Model):
    """
    Quest playable by a player character.
    """
    quest_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent unique quest number.",
        verbose_name="Quest ID"
    )
    name = models.CharField(
        unique=True,
        max_length=25,
        help_text="Internal name of the quest.",
        verbose_name="Name"
    )
    display_name = models.CharField(
        max_length=30,
        help_text="Friendly display name of the quest.",
        verbose_name="Display Name"
    )
    completion_message = models.CharField(
        blank=True,
        max_length=700,
        help_text="Message sent to the player upon completion of the quest.",
        verbose_name="Completion Message"
    )
    min_level = models.IntegerField(
        help_text="Minimum level of a player that may partake in the quest.",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=max(settings.IMMORTAL_LEVELS))
        ],
        verbose_name="Minimum Level"
    )
    max_level = models.IntegerField(
        help_text="Maximum level of a player that may partake in the quest.",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=max(settings.IMMORTAL_LEVELS))
        ],
        verbose_name="Maximum Level"
    )
    repeatable = models.BooleanField(
        help_text="Is the quest repeatable?",
        verbose_name="Repeatable?"
    )
    description = models.CharField(
        blank=True, max_length=512, null=True,
        help_text="Description of the quest.",
        verbose_name="Description"
    )
    prerequisite = models.IntegerField(
        help_text="Prerequisite of the quest.",
        verbose_name="Prerequisite"
    )
    class_restrict = models.IntegerField(
        choices=get_class_options(),
        help_text="Player class to which the quest is restricted.",
        verbose_name="Class Restrict"
    )
    quest_intro = models.CharField(
        blank=True, max_length=2000,
        help_text="Introduction text for the quest.",
        verbose_name="Quest Intro"
    )
    quest_source = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Source for the quest.",
        verbose_name="Quest Source"
    )
    quest_return = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Return for the quest.",
        verbose_name="Quest Return"
    )

    class Meta:
        db_table = "quests"
        default_related_name = "quest"
        managed = False
        ordering = ("-repeatable", "-class_restrict", "display_name")
        verbose_name = "Quest"

    def __repr__(self) -> str:
        return f'Quest: "{self.__str__()}" ({self.quest_id})'

    def __str__(self) -> str:
        return self.display_name or self.name or self.quest_id

    @property
    @admin.display(description="# Pre-Requisites")
    def prereq_count(self) -> int:
        """
        Number of prerequisites within the quest.
        """
        return self.steps.count()

    @property
    @admin.display(description="# Steps")
    def step_count(self) -> int:
        """
        Number of steps within the quest.
        """
        return self.steps.count()

    @property
    @admin.display(description="Levels")
    def for_levels(self) -> str:
        """
        String of the level range of the quest.
        """
        return f"{self.min_level} - {self.max_level}"
