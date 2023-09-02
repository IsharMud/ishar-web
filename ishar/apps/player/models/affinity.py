from django.db import models


class RacialAffinity(models.Model):
    """
    Racial Affinity.
    """
    race = models.ForeignKey(
        to=Race,
        on_delete=models.CASCADE,
        help_text="Race of the racial affinity.",
        related_name="affinities",
        related_query_name="affinity",
        verbose_name="Affinity Type"
    )
    force = models.ForeignKey(
        to=Force,
        on_delete=models.CASCADE,
        help_text="Force of the racial affinity.",
        verbose_name="Force"
    )
    affinity_type = models.IntegerField(
        help_text="Type of racial affinity.",
        verbose_name="Affinity Type"
    )

    class Meta:
        managed = False
        db_table = "racial_affinities"
        default_related_name = "affinity"
        ordering = ("affinity_type",)
        verbose_name = "Racial Affinity"
        verbose_name_plural = "Racial Affinities"
