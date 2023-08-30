from django.db import models
from django.contrib import admin


class Season(models.Model):
    """
    Ishar Season.
    """
    season_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent season (identification) number.",
        verbose_name="Season ID"
    )
    is_active = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Is the season active?",
        verbose_name="Is Active?"
    )
    effective_date = models.DateTimeField(
        help_text="Effective start date of the season.",
        verbose_name="Effective Date"
    )
    expiration_date = models.DateTimeField(
        help_text="Expiration end date of the season.",
        verbose_name="Expiration Date"
    )
    last_challenge_cycle = models.DateTimeField(
        help_text="Last date and time of challenges cycled in the season.",
        verbose_name="Last Challenge Cycle"
    )
    average_essence_gain = models.FloatField(
        help_text="Average essence gain in the season.",
        verbose_name="Average Essence Gain"
    )
    average_remorts = models.FloatField(
        help_text="Average remorts in the season.",
        verbose_name="Average Remorts"
    )
    max_essence_gain = models.IntegerField(
        help_text="Max essence gain in the season.",
        verbose_name="Max Essence Gain"
    )
    max_remorts = models.IntegerField(
        help_text="Max number of remorts in the season.",
        verbose_name="Max Remorts"
    )
    season_leader_account = models.IntegerField(
        blank=True, null=True,
        help_text="Leader account in the season.",
        verbose_name="Season Leader Account"
    )
    seasonal_leader_name = models.TextField(
        blank=True, null=True,
        help_text="Leader name in the season.",
        verbose_name="Seasonal Leader Name"
    )
    max_renown = models.IntegerField(
        help_text="Max amount of renown gained in the season.",
        verbose_name="Max Renown"
    )
    avg_renown = models.FloatField(
        help_text="Average amount of renown gained in the season.",
        verbose_name="Average Renown"
    )

    class Meta:
        managed = False
        db_table = 'seasons'
        ordering = ("-is_active", "-season_id")
        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Season {self.season_id}"

    @admin.display(boolean=True, description="Active?", ordering="is_active")
    def _is_active(self) -> bool:
        """
        Boolean whether the season is active.
        """
        if self.is_active == 1:
            return True
        return False
