from django.db import models

from . import Quest
from ishar.util.player import get_class_options


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
            (0, "Object_always"), (1, "Object_Choice"), (2, "Money"),
            (3, "Alignment"), (4, "Skill"), (5, "Renown"), (6, "Experience"),
            (7, "Quest"), (8, "Relic")
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
        on_delete=models.DO_NOTHING,
        related_name="rewards",
        related_query_name="reward",
        verbose_name="Quest"
    )
    class_restrict = models.IntegerField(
        choices=get_class_options(),
        help_text="Player class which the reward is restricted to.",
        verbose_name="Class Restrict"
    )

    # The composite primary key (reward_num, quest_id) found,
    #   that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = "quest_rewards"
        default_related_name = "reward"
        ordering = ("quest", "quest_reward_id")
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
