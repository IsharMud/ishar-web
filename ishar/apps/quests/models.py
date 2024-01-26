from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from ishar.apps.classes.models import PLAYER_CLASSES


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
            MaxValueValidator(limit_value=max(settings.IMMORTAL_LEVELS)[0])
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
            MaxValueValidator(limit_value=max(settings.IMMORTAL_LEVELS)[0])
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
        choices=PLAYER_CLASSES,
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

    class Meta:
        db_table = "quests"
        default_related_name = "quest"
        managed = False
        ordering = ("display_name",)
        verbose_name = "Quest"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())}"
            f" ({self.quest_id})"
        )

    def __str__(self) -> str:
        return self.display_name or self.name


class QuestPrereq(models.Model):
    """
    Quest Prerequisite.
    """
    quest_prereqs_id = models.AutoField(
        blank=False,
        db_column="quest_prereqs_id",
        help_text="Auto-generated, permanent quest pre-requisite relation ID.",
        primary_key=True,
        null=False,
        verbose_name="Quest Prerequisite ID"
    )
    quest = models.ForeignKey(
        to=Quest,
        on_delete=models.CASCADE,
        db_column="quest_id",
        help_text="Quest which requires a prerequisite.",
        verbose_name="Quest"
    )
    required_quest = models.ForeignKey(
        to=Quest,
        on_delete=models.CASCADE,
        db_column="required_quest",
        help_text="Prerequisite quest, required prior to another quest.",
        related_name="questprereq_required_quest_set",
        verbose_name="Required Quest"
    )

    class Meta:
        managed = False
        db_table = "quest_prereqs"
        ordering = ("quest", "required_quest")
        verbose_name = "Prerequisite"
        verbose_name_plural = "Prerequisites"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())} "
            f" ({self.quest_prereqs_id})"
        )

    def __str__(self) -> str:
        return f"{self.quest} requires {self.required_quest}"


class QuestReward(models.Model):
    """
    Quest Reward.
    """
    quest_reward_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated, permanent quest reward ID number.",
        verbose_name="Quest Reward ID"
    )
    reward_type = models.IntegerField(
        choices=(
            (0, "Object (Always) [0]"),
            (1, "Object (Choice) [1]"),
            (2, "Money [2]"),
            (3, "Alignment [3]"),
            (4, "Skill [4]"),
            (5, "Renown [5]"),
            (6, "Experience [6]"),
            (7, "Quest [7]"),
            (8, "Relic [8]")
        ),
        help_text="Reward type.",
        verbose_name="Reward Type"
    )
    reward_num = models.IntegerField(
        help_text="Amount/value/target number of the reward.",
        verbose_name="Reward Number"
    )
    quest = models.ForeignKey(
        to=Quest,
        db_column="quest_id",
        help_text="Quest which the reward is for.",
        on_delete=models.CASCADE,
        related_name="rewards",
        related_query_name="reward",
        verbose_name="Quest"
    )
    class_restrict = models.IntegerField(
        choices=PLAYER_CLASSES,
        help_text="Player class which the reward is restricted to.",
        verbose_name="Class Restrict"
    )

    # The composite primary key (reward_num, quest_id) found,
    #   that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = "quest_rewards"
        default_related_name = "reward"
        ordering = ("quest_reward_id",)
        verbose_name = "Reward"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__} [{self.quest_reward_id}]: "
            f"{repr(self.__str__())}"
        )

    def __str__(self) -> str:
        return (
            f"({self.get_reward_type_display()}) {self.reward_num} "
            f"@ {self.quest}"
        )


class QuestStep(models.Model):
    """
    Quest Step.
    """
    step_id = models.AutoField(
        primary_key=True,
        help_text="Quest step identification number",
        verbose_name="Quest Step ID"
    )
    step_type = models.IntegerField(
        choices=(
            (0, "Object [0]"),
            (1, "Kill [1]"),
            (2, "Room [2]")
        ),
        help_text="Quest step type.",
        verbose_name="Step Type",
    )
    target = models.IntegerField(
        help_text="Target of the quest step.",
        verbose_name="Target"
    )
    num_required = models.IntegerField(
        help_text="Number required for the quest step.",
        verbose_name="Number Required"
    )
    quest = models.ForeignKey(
        null=False,
        to=Quest,
        on_delete=models.CASCADE,
        related_name='steps',
        related_query_name='step',
        help_text="Quest related to the quest step.",
        verbose_name="Quest"
    )
    time_limit = models.IntegerField(
        help_text="Time limit for the quest step.",
        verbose_name="Time Limit"
    )
    mystify = models.BooleanField(
        help_text="Mystify Quest Step.",
        verbose_name="Mystify"
    )
    mystify_text = models.CharField(
        blank=True,
        max_length=80,
        help_text="Mystify text for the quest step.",
        verbose_name="Mystify Text"
    )

    class Meta:
        managed = False
        db_table = "quest_steps"
        default_related_name = "step"
        ordering = ("step_id",)
        verbose_name = "Step"
        verbose_name_plural = "Steps"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__} [{self.step_id}]: "
            f"{repr(self.__str__())}"
        )

    def __str__(self) -> str:
        return (
            f"({self.get_step_type_display()}) {self.target} "
            f"x{self.num_required} @ {self.quest}"
        )
