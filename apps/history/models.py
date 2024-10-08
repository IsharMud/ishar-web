from datetime import timedelta

from django.db import models
from django.utils.timesince import timesince
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from apps.accounts.models.account import Account
from apps.classes.models.cls import Class
from apps.players.models.game_type import GameType
from apps.races.models.race import Race
from apps.seasons.models.season import Season


class HistoricSeasonStat(models.Model):
    """Historical season statistic."""

    season = models.ForeignKey(
        to=Season,
        to_field="season_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Season related to the historic statistic."),
        verbose_name=_("Season"),
        related_name="+"
    )
    account = models.ForeignKey(
        to=Account,
        to_field="account_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Account related to the historic statistic."),
        verbose_name=_("Account"),
        related_name="+"
    )
    player_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Player name related to the historic statistic."),
        verbose_name=_("Player Name")
    )
    remorts = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Remorts related to the historic statistic."),
        verbose_name=_("Remorts")
    )
    player_class = models.ForeignKey(
        to=Class,
        to_field="class_id",
        on_delete=models.DO_NOTHING,
        db_column="class_id",
        blank=True,
        null=True,
        help_text=_("Player class related to the historic statistic."),
        verbose_name=_("Player Class"),
        related_name="+"
    )
    race = models.ForeignKey(
        to=Race,
        to_field="race_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Player race related to the historic statistic."),
        verbose_name=_("Player Race"),
        related_name="+"
    )
    total_renown = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Total renown related to the historic statistic."),
        verbose_name=_("Total Renown")
    )
    challenges_completed = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Challenges completed related to the historic statistic."),
        verbose_name=_("Challenges Completed")
    )
    quests_completed = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Quests completed related to the historic statistic."),
        verbose_name=_("Quests Completed")
    )
    deaths = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Deaths related to the historic statistic."),
        verbose_name=_("Deaths")
    )
    game_type = models.PositiveIntegerField(
        blank=True,
        choices=GameType,
        null=True,
        help_text=_("Game type related to the historic statistic."),
        verbose_name=_("Game Type")
    )
    play_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Play time related to the historic statistic."),
        verbose_name=_("Play Time")
    )
    level = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Level related to the historic statistic."),
        verbose_name=_("Level")
    )

    class Meta:
        managed = False
        db_table = "historic_season_stat"
        default_related_name = "+"
        ordering = (
            "-season__pk",
            "-remorts",
            "-challenges_completed",
            "-quests_completed",
            "deaths",
            "-level"
        )
        verbose_name = "Season Statistic"
        verbose_name_plural = "Season Statistics"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return f"{self.account} - {self.player_name} @ {self.season}"

    def get_total_play_timedelta(self):
        return timedelta(seconds=self.play_time or 0)

    def get_total_play_time(self):
        return timesince(localtime() - self.get_total_play_timedelta())

    def display_total_play_time(self):
        return (
            f"{self.get_total_play_time()} ({self.get_total_play_timedelta()})"
        )
