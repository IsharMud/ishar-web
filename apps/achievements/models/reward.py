from django.db import models
from django.utils.translation import gettext_lazy as _

from .achievement import Achievement


class AchievementRewardType(models.IntegerChoices):
    """Achievement reward type choices."""

    NEGATIVE_ONE = -1
    ACHIEVEMENT_POINTS = 0
    ESSENCE = 1
    SOULBOUND_ITEM = 2
    TITLE = 3

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()


class AchievementReward(models.Model):
    """Ishar achievement reward."""

    reward_id = models.AutoField(
        db_column="reward_id",
        help_text=_("Achievement reward identification number primary key."),
        primary_key=True,
        verbose_name=_("Achievement Reward ID"),
    )
    achievement = models.ForeignKey(
        blank=True,
        db_column="achievement_id",
        null=True,
        to=Achievement,
        to_field="achievement_id",
        on_delete=models.DO_NOTHING,
        help_text=_("Achievement related to the reward."),
        verbose_name=_("Achievement")
    )
    reward_type = models.PositiveIntegerField(
        blank=True,
        choices=AchievementRewardType,
        null=True,
        help_text=_("Type of the achievement reward."),
        verbose_name=_("Type")
    )
    reward_value = models.IntegerField(
        blank=True,
        null=True,
        help_text="Value of the achievement reward",
        verbose_name=_("Value")
    )

    class Meta:
        managed = False
        db_table = "achievement_rewards"
        default_related_name = "reward"
        ordering = ("achievement", "reward_type",)
        verbose_name = _("Achievement Reward")
        verbose_name_plural = _("Achievement Rewards")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return (
            f"{self.get_reward_type_display()} ({self.reward_value})"
            f" @ {self.achievement}"
        )
