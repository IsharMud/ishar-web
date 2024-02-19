from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from ishar.apps.classes.models.type import PlayerClass


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
            MaxValueValidator(limit_value=settings.MAX_IMMORTAL_LEVEL)
        ],
        verbose_name="Minimum Level"
    )
    deprecated_max_level = models.IntegerField(
        default=20,
        editable=False,
        db_column="max_level",
        help_text="(Deprecated) Maximum level of player that may do the quest.",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=settings.MAX_IMMORTAL_LEVEL)
        ],
        verbose_name="Maximum Level (Deprecated)"
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
    deprecated_prerequisite = models.IntegerField(
        default="-1",
        editable=False,
        db_column="prerequisite",
        help_text="(Deprecated) Prerequisite of the quest.",
        verbose_name="Prerequisite (Deprecated)"
    )
    class_restrict = models.IntegerField(
        choices=PlayerClass,
        help_text="Player class which the quest is restricted to.",
        verbose_name="Class Restrict"
    )
    quest_intro = models.CharField(
        blank=True,
        max_length=2000,
        null=True,
        help_text="Introduction text for the quest.",
        verbose_name="Quest Intro"
    )
    quest_source = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Source for the quest.",
        verbose_name="Quest Source"
    )
    quest_return = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Return for the quest.",
        verbose_name="Quest Return"
    )
    start_item = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        help_text="Start item for the quest.",
        verbose_name="Start Item"
    )

    class Meta:
        db_table = "quests"
        default_related_name = "quest"
        managed = False
        ordering = ("display_name",)
        verbose_name = "Quest"

    def __repr__(self) -> str:
        return "%s %s (%d)" % (self.__class__.__name__, self.__str__(), self.pk)

    def __str__(self) -> str:
        return self.display_name or self.name
