from django.db import models

from apps.skills.models.force import Force

from .race import Race
from .type import AffinityType


class RaceAffinity(models.Model):
    """Ishar race affinity."""

    race_affinity_id = models.AutoField(
        blank=False,
        help_text="Primary identification number of the race affinity.",
        null=False,
        primary_key=True,
        verbose_name="Race Affinity ID",
    )
    race = models.ForeignKey(
        to=Race,
        on_delete=models.DO_NOTHING,
        help_text="Race of the affinity.",
        related_name="affinities",
        related_query_name="affinity",
        verbose_name="Race",
    )
    force = models.ForeignKey(
        to=Force,
        on_delete=models.DO_NOTHING,
        help_text="Force of the affinity.",
        verbose_name="Force",
    )
    affinity_type = models.IntegerField(
        choices=AffinityType,
        help_text="Type of race affinity.",
        verbose_name="Affinity Type",
    )

    class Meta:
        managed = False
        db_table = "racial_affinities"
        default_related_name = "affinity"
        ordering = ("race", "force", "affinity_type")
        verbose_name = "Affinity"
        verbose_name_plural = "Affinities"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return (
            f"{self.force} @ {self.race}"
            f" / {self.get_affinity_type_display()} ({self.affinity_type})"
        )
