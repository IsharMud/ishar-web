from django.db import models

from .achievement import Achievement


class AchievementReward(models.Model):
    """Ishar achievement reward."""
    reward_id = models.PositiveIntegerField(
        db_column="reward_id",
        help_text="Achievement reward identification number primary key.",
        primary_key=True,
        verbose_name="Achievement Reward ID",
    )
    achievement = models.ForeignKey(
        blank=True,
        db_column="achievement_id",
        null=True,
        to=Achievement,
        to_field="achievement_id",
        on_delete=models.DO_NOTHING,
        help_text="Achievement related to the reward.",
        verbose_name="Achievement"
    )
    reward_type = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Type of the achievement reward.",
        verbose_name="Type"
    )
    reward_value = models.IntegerField(
        blank=True,
        null=True,
        help_text="Value of the achievement reward",
        verbose_name="Value"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the achievement reward.",
        verbose_name="Description"
    )

    class Meta:
        managed = False
        db_table = 'achievement_rewards'
        default_related_name = "reward"
        ordering = ("achievement", "reward_type",)
        verbose_name = "Achievement Reward"
        verbose_name_plural = "Achievement Rewards"

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return "%s (%s) @ %s" % (
            self.reward_type,
            self.reward_value,
            self.achievement
        )
