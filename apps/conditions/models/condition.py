from django.db import models
from django.utils.translation import gettext_lazy as _


class ConditionManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key by condition name.
        return self.get(name=name)


class Condition(models.Model):
    """Ishar condition."""

    objects = ConditionManager()

# TODO: This column is not actually autoincrement.
#    condition_id = models.AutoField(
#        primary_key=True,
#        help_text=_(
#            "Auto-generated primary identification number of the condition."
#        ),
#        verbose_name="Condition ID",
#    )

    condition_id = models.PositiveIntegerField(
        primary_key=True,
        help_text=_("Primary identification number of the condition."),
        verbose_name="Condition ID",
    )
    name = models.CharField(
        max_length=20,
        blank=True,
        help_text="Name of the condition.",
        null=False,
        unique=True,
        verbose_name="Name",
    )

    class Meta:
        managed = False
        db_table = "conditions"
        ordering = ("condition_id",)
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name

    def natural_key(self) -> str:
        # Natural key by name.
        return self.name
