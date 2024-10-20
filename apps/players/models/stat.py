from datetime import timedelta

from django.db import models
from django.utils.timesince import timesince
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from .player import PlayerBase


class PlayerStat(models.Model):
    """Ishar player statistics."""

    player_stats_id = models.AutoField(
        primary_key=True,
        help_text=_("Player statistics primary key identification number."),
        verbose_name=_("Player Stats ID"),
    )
    player = models.OneToOneField(
        to=PlayerBase,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="statistics",
        related_query_name="statistics",
        help_text=_("Player related to the statistics"),
        verbose_name=_("Player"),
    )
    total_play_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The total play time statistic for the player."),
        verbose_name=_("Total Play Time"),
    )
    remort_play_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The remort play time statistic for the player."),
        verbose_name=_("Remort Play Time"),
    )
    total_deaths = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Total number of deaths statistic for the player."),
        verbose_name=_("Total Deaths"),
    )
    remort_deaths = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The number of remort deaths statistic for the player."),
        verbose_name=_("Remort Deaths"),
    )
    total_renown = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The number of total renown statistic for the player."),
        verbose_name=_("Total Renown"),
    )
    remort_renown = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The number of remort renown statistic for the player."),
        verbose_name=_("Remort Renown"),
    )
    total_challenges = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The number of total challenges statistic for the player."),
        verbose_name=_("Total Challenges"),
    )
    remort_challenges = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_(
            "The number of remort challenges statistic for the player."
        ),
        verbose_name=_("Remort Challenges"),
    )
    total_quests = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The number of total quests statistic for the player."),
        verbose_name=_("Total Quests"),
    )
    remort_quests = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("The number of remort quests statistic for the player."),
        verbose_name=_("Remort Quests"),
    )

    class Meta:
        managed = False
        db_table = "player_stats"
        default_related_name = "statistics"
        ordering = ("player",)
        verbose_name = verbose_name_plural = _("Player Statistics")

    def __repr__(self) -> str:
        return f"{self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.player}"

    def get_remort_play_timedelta(self) -> timedelta:
        # Timedelta of player remort play time.
        return timedelta(seconds=self.remort_play_time or 0)

    def get_total_play_timedelta(self) -> timedelta:
        # Timedelta of player total play time.
        return timedelta(seconds=self.total_play_time or 0)

    def get_remort_play_time(self) -> timedelta:
        # Time to calculate since, for remort play time.
        return timesince(localtime() - self.get_remort_play_timedelta())

    def get_total_play_time(self) -> timedelta:
        # Time to calculate since, for total play time.
        return timesince(localtime() - self.get_total_play_timedelta())
