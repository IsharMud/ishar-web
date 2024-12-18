from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .race import Race


class RaceDeathload(models.Model):
    """Ishar race deathload."""

    id = models.AutoField(
        db_column="racial_deathload_id",
        help_text="Primary identification number of the race deathload.",
        primary_key=True,
        verbose_name="Race Deathload ID",
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
        verbose_name="Race",
    )
    vnum = models.PositiveIntegerField(
        blank=False,
        help_text="VNUM of the race deathload.",
        null=False,
        verbose_name="VNUM",
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
        verbose_name="Percent Chance",
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
        verbose_name="Minimum Level",
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
        verbose_name="Maximum Level",
    )
    max_load = models.PositiveIntegerField(
        blank=True,
        default=1,
        help_text="Maximum load number of the race deathload.",
        null=True,
        verbose_name="Maximum Load",
    )

    class Meta:
        db_table = "racial_deathload"
        default_related_name = "deathload"
        managed = False
        ordering = ("race", "vnum", "percent_chance", "min_level")
        verbose_name = "Deathload"
        verbose_name_plural = "Deathloads"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.vnum} @ {self.race}"
