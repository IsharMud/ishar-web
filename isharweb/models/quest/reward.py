from django.db import models

from . import Quest


class QuestReward(models.Model):
    """
    Quest Reward.
    """
    reward_num = models.IntegerField(
        primary_key=True,
        help_text="Reward number.",
        verbose_name="Reward Number"
    )
    reward_type = models.IntegerField(
        choices=[
            (0, "Object_always"), (1, "Object_Choice"), (2, "Money"),
            (3, "Alignment"), (4, "Skill"), (5, "Renown"), (6, "Experience"),
            (7, "Quest")
        ],
        help_text="Reward type.",
        verbose_name="Reward Type"
    )
    quest = models.ForeignKey(
        to=Quest,
        help_text="Quest to which the reward is for.",
        on_delete=models.DO_NOTHING,
        related_name='rewards',
        related_query_name='reward',
        verbose_name="Quest"
    )
    class_restrict = models.IntegerField(
        choices=[(-1, "None")],  # TODO: Fill this in. (Automatically?)
        help_text="Player class to which the reward is restricted.",
        verbose_name="Class Restrict"
    )

    # The composite primary key (reward_num, quest_id) found,
    #   that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = "quest_rewards"
        ordering = ("quest", "reward_type", "class_restrict", "reward_num")
        unique_together = (("reward_num", "quest"),)
        verbose_name = "Quest Reward"
        verbose_name_plural = "Quest Rewards"

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return (
            f"Quest Reward: {self.get_reward_type_display()} @ {self.quest}"
        )
