from django.db import models
from django.utils.translation import gettext_lazy as _

from .achievement import Achievement


class AchievementCriteria(models.Model):
    """Ishar achievement criteria."""
    criteria_id = models.AutoField(
        db_column="criteria_id",
        help_text=_(
            "Auto-generated, permanent achievement criteria identification "
            "number primary key."
        ),
        primary_key=True,
        verbose_name=_("Achievement Criteria ID"),
    )
    achievement = models.ForeignKey(
        blank=True,
        db_column="achievement_id",
        null=True,
        to=Achievement,
        to_field="achievement_id",
        on_delete=models.DO_NOTHING,
        help_text="Achievement related to a criteria.",
        verbose_name="Achievement"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the achievement criteria.",
        verbose_name="Description"
    )
    criteria_type = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Type of the achievement criteria.",
        verbose_name="Type"
    )
    target_value = models.IntegerField(
        blank=True,
        null=True,
        help_text="Target value of the achievement criteria",
        verbose_name="Target"
    )

    class Meta:
        managed = False
        db_table = "achievement_criteria"
        default_related_name = "criteria"
        ordering = ("achievement", "criteria_type",)
        verbose_name = verbose_name_plural = "Achievement Criteria"

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return "%s (%s) @ %s" % (
            self.criteria_type,
            self.target_value,
            self.achievement
        )
