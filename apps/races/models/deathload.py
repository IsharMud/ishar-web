from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from .race import Race
from ...classes.models.cls import Class


class RaceDeathload(models.Model):
    """Ishar race deathload."""

    id = models.AutoField(
        db_column="racial_deathload_id",
        help_text="Primary identification number of the race deathload.",
        primary_key=True,
        verbose_name=_("Race Deathload ID"),
    )
    race = models.ForeignKey(
        blank=False,
        db_column="race_id",
        to=Race,
        on_delete=models.DO_NOTHING,
        null=False,
        help_text="Race related to the deathload.",
        related_name="deathloads",
        related_query_name="deathload",
        verbose_name=_("Race"),
    )
    vnum = models.PositiveIntegerField(
        blank=False,
        help_text="VNUM of the race deathload.",
        null=False,
        verbose_name=_("VNUM"),
    )
    percent_chance = models.PositiveIntegerField(
        blank=False,
        default=0,
        help_text="Percent chance of the race deathload.",
        null=False,
        validators=(
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=100),
        ),
        verbose_name=_("Percent Chance"),
    )
    min_level = models.PositiveIntegerField(
        blank=False,
        default=1,
        help_text="Minimum level of the race deathload.",
        null=False,
        validators=(
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=30),
        ),
        verbose_name=_("Minimum Level"),
    )
    max_level = models.PositiveIntegerField(
        blank=True,
        default=30,
        help_text="Maximum level of the race deathload.",
        null=True,
        validators=(
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=30),
        ),
        verbose_name=_("Maximum Level"),
    )

    min_quantity = models.PositiveIntegerField(
        blank=True,
        default=1,
        help_text=_("Minimum number of this item to load"),
        null=False,
        verbose_name=_("Minimum Quantity"),
    )
    max_quantity = models.PositiveIntegerField(
        blank=True,
        help_text=_("Maximum number of this item to load"),
        null=True,
        verbose_name=_("Maximum Quantity"),
    )
    class_restrict = models.ForeignKey(
        blank=True,
        db_column="class_restrict",
        default=4,
        to=Class,
        on_delete=models.CASCADE,
        null=True,
        help_text=_("Class which the deathload is restricted to."),
        related_name="deathloads",
        related_query_name="deathload",
        verbose_name=_("Class Restrict"),
    )

    class Meta:
        db_table = "racial_deathload"
        default_related_name = "deathload"
        managed = False
        ordering = ("race", "vnum", "percent_chance", "min_level")
        verbose_name = _("Deathload")
        verbose_name_plural = _("Deathloads")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.vnum} @ {self.race} : {self.class_restrict}"
