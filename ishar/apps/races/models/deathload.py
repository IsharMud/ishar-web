from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from .race import Race


class RaceDeathload(models.Model):
    """
    Race Deathload.
    """
    id = models.AutoField(
        blank=False,
        db_column="racial_deathload_id",
        help_text="Primary identification number of the race deathload.",
        null=False,
        primary_key=True,
        verbose_name="Race Deathload ID"
    )
    race = models.ForeignKey(
        blank=False,
        db_column="race_id",
        to=Race,
        on_delete=models.CASCADE,
        null=False,
        help_text="Race related to the deathload.",
        related_name="deathloads",
        related_query_name="deathload",
        verbose_name="Race"
    )
    vnum = models.PositiveIntegerField(
        blank=False,
        help_text="VNUM of the race deathload.",
        null=False,
        verbose_name="VNUM"
    )
    percent_chance = models.PositiveIntegerField(
        blank=False,
        default=0,
        help_text="Percent chance of the race deathload.",
        null=False,
        validators=(
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=100)
        ),
        verbose_name="Percent Chance"
    )
    min_level = models.PositiveIntegerField(
        blank=False,
        default=1,
        help_text="Minimum level of the race deathload.",
        null=False,
        validators=(
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=max(settings.IMMORTAL_LEVELS)[0])
        ),
        verbose_name="Minimum Level"
    )

    class Meta:
        db_table = "racial_deathload"
        default_related_name = "deathload"
        managed = False
        ordering = ("race", "vnum", "percent_chance", "min_level")
        verbose_name = "Deathload"
        verbose_name_plural = "Deathloads"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.pk
        )

    def __str__(self):
        return "%i @ %s" % (self.vnum, self.race)
