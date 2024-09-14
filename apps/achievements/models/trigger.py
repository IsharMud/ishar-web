from django.db import models
from django.utils.translation import gettext_lazy as _

from .achievement import Achievement
from .type.trigger import AchievementTriggerType


class AchievementTrigger(models.Model):
    """Ishar achievement trigger."""
    achievement_triggers_id = models.AutoField(
        help_text=_("Achievement trigger identification number primary key."),
        primary_key=True,
        verbose_name=_("Achievement Trigger ID"),
    )
    achievement = models.ForeignKey(
        blank=True,
        null=True,
        to=Achievement,
        to_field="achievement_id",
        on_delete=models.DO_NOTHING,
        help_text=_("Achievement related to a trigger."),
        verbose_name=_("Achievement")
    )
    trigger_type = models.CharField(
        blank=True,
        choices=AchievementTriggerType,
        max_length=18,
        null=True,
        help_text=_("Type of achievement trigger."),
        verbose_name=_("Trigger Type")
    )

    class Meta:
        managed = False
        db_table = "achievement_triggers"
        default_related_name = "trigger"
        ordering = ("achievement", "trigger_type",)
        verbose_name = _("Achievement Trigger")
        verbose_name_plural = _("Achievement Triggers")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.trigger_type} @ {self.achievement}"
