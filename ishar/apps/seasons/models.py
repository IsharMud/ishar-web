from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import now


class Season(models.Model):
    """
    Season.
    """
    season_id = models.PositiveIntegerField(
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
        db_table = "seasons"
        default_related_name = "season"
        ordering = ("-season_id",)
        verbose_name = "Season"

    def __repr__(self) -> str:
        return "%s: %s" % (
            self.__class__.__name__,
            self.__str__()
        )

    def __str__(self) -> str:
        dt_fmt = "%a, %b %d, %Y"
        return "%i (%s - %s)" % (
            self.season_id,
            self.effective_date.strftime(dt_fmt),
            self.expiration_date.strftime(dt_fmt),
        )

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="season",
            args=(self.season_id,)
        )

    def get_admin_link(self) -> str:
        return format_html(
            '<a href="%s" title="%s">%s</a>' % (
                self.get_admin_url(),
                self.__repr__(),
                self.__repr__(),
            )
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
                    add_time = timedelta(days=7)
                    return self.last_challenge_cycle + add_time
        return None
