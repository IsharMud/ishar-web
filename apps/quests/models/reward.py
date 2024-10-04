from django.db import models

from apps.classes.models.type import PlayerClass

from .quest import Quest


class QuestRewardType(models.IntegerChoices):
    """Quest reward type choices."""

    NEGATIVE_ONE = -1
    OBJECT_ALWAYS = 0, "Object (Always)"
    OBJECT_CHOICE = 1, "Object (Choice)"
    MONEY = 2
    ALIGNMENT = 3
    SKILL = 4
    RENOWN = 5
    EXPERIENCE = 6
    QUEST = 7
    RELIC = 8

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()


class QuestReward(models.Model):
    """Ishar quest reward."""

    quest_reward_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated, permanent quest reward ID number.",
        verbose_name="Quest Reward ID"
    )
    reward_type = models.IntegerField(
        choices=QuestRewardType,
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
        on_delete=models.DO_NOTHING,
        related_name="rewards",
        related_query_name="reward",
        verbose_name="Quest"
    )
    class_restrict = models.IntegerField(
        choices=PlayerClass,
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
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return (
            f"{self.get_reward_type_display()} ({self.reward_num})"
            f" @ {self.quest}"
        )
