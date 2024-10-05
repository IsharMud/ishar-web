from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import now


class Season(models.Model):
    """Ishar season."""
    season_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent season (identification) number.",
        verbose_name="Season ID"
    )
    is_active = models.BooleanField(
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
        blank=True,
        null=True,
        help_text="Leader account in the season.",
        verbose_name="Season Leader Account"
    )
    seasonal_leader_name = models.TextField(
        blank=True,
        null=True,
        help_text="Leader name in the season.",
        verbose_name="Seasonal Leader Name"
    )
    last_challenge_cycle = models.DateTimeField(
        help_text="Last date and time of challenges cycled in the season.",
        verbose_name="Last Challenge Cycle"
    )
    max_renown = models.IntegerField(
        help_text="Max amount of renown gained in the season.",
        verbose_name="Max Renown"
    )
    avg_renown = models.FloatField(
        help_text="Average amount of renown gained in the season.",
        verbose_name="Average Renown"
    )
    total_remorts = models.IntegerField(
        help_text="Total number of remorts in the season.",
        verbose_name="Total Remorts"
    )
    game_state = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Game state of the season.",
        verbose_name="Game State"
    )
    multiplay_limit = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Limit of players that one account can log in to.",
        verbose_name="Multi-Play Limit"
    )

    class Meta:
        managed = False
        db_table = "seasons"
        default_related_name = "season"
        get_latest_by = ("is_active", "season_id")
        ordering = ("-is_active", "-season_id",)
        verbose_name = "Season"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        dt_fmt = "%a, %b %d, %Y"
        return (
            f"{self.season_id} ({self.effective_date.strftime(dt_fmt)}"
            f" - {self.expiration_date.strftime(dt_fmt)})"
        )

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="season",
            args=(self.season_id,)
        ) + "#season"

    def get_admin_link(self) -> str:
        return format_html(
            '<a href="{}" title="{}">{}</a>',
            self.get_admin_url(),
            self.__repr__(),
            self.__repr__()
        )

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:seasons_season_change",
            args=(self.season_id,)
        )

    def get_next_cycle(self) -> (datetime, None):
        """Cycle of challenges is X amount of time after last cycle."""
        if self.last_challenge_cycle:
            if isinstance(self.last_challenge_cycle, datetime):
                if self.last_challenge_cycle <= now():
                    return self.last_challenge_cycle + timedelta(days=7)
        return None
