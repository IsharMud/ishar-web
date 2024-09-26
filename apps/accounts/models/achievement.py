from django.db import models

from apps.achievements.models.achievement import Achievement
from apps.objects.models.object import Object

from .account import Account


class AccountAchievement(models.Model):
    """Ishar account achievement."""
    account_achievement_id = models.AutoField(
        primary_key=True,
        help_text=(
            "Auto-generated, primary key identification number of the account "
            "achievement relation."
        ),
        verbose_name="Account Achievement ID"
    )
    achievement = models.ForeignKey(
        blank=True,
        db_column="achievement_id",
        null=True,
        to=Achievement,
        to_field="achievement_id",
        on_delete=models.DO_NOTHING,
        help_text="Achievement related to an account.",
        verbose_name="Achievement"
    )
    is_completed = models.IntegerField(
        blank=True,
        null=True,
        help_text="Has the achievement been completed by the account?",
        verbose_name="Is Completed?"
    )
    completion_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The completion date of the achievement by the account.",
        verbose_name="Completion Date"
    )
    account = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        to=Account,
        help_text="Account related to an achievement.",
        verbose_name="Account"
    )

    completed_by = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Account achievement completed by.",
        verbose_name="Completed By"
    )

    class Meta:
        managed = False
        db_table = "account_achievements"
        default_related_name = "achievement"
        ordering = ("achievement", "account",)
        verbose_name = "Account Achievement"
        verbose_name_plural = "Account Achievements"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) ->str:
        return f"{self.achievement} @ {self.account}"
