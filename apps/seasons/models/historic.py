from django.db import models

from apps.classes.models.cls import Class
from apps.players.models.game_type import GameType
from apps.races.models.race import Race

from .season import Season


class HistoricSeasonStat(models.Model):
    """Per-player snapshot of a completed season, written by the game's
    season cycle (`cycle_season`, ishar-mud src/dbase/season.c) just before
    it deletes the season's mortal players. Read-only season history."""

    id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent historic season stat number.",
        verbose_name="Historic Season Stat ID",
    )
    season = models.ForeignKey(
        blank=True,
        null=True,
        to=Season,
        on_delete=models.DO_NOTHING,
        related_name="historic_stats",
        related_query_name="historic_stat",
        help_text="Season which the player snapshot was taken for.",
        verbose_name="Season",
    )
    account = models.ForeignKey(
        blank=True,
        null=True,
        to="accounts.Account",
        on_delete=models.DO_NOTHING,
        related_name="historic_season_stats",
        related_query_name="historic_season_stat",
        help_text="Account that owned the player character.",
        verbose_name="Account",
    )
    player_name = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        help_text="Name of the player character.",
        verbose_name="Player Name",
    )
    remorts = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of remorts the player finished the season with.",
        verbose_name="Remorts",
    )
    player_class = models.ForeignKey(
        blank=True,
        db_column="class_id",
        null=True,
        to=Class,
        on_delete=models.DO_NOTHING,
        related_query_name="+",
        help_text="Class of the player character.",
        verbose_name="Class",
    )
    race = models.ForeignKey(
        blank=True,
        null=True,
        to=Race,
        on_delete=models.DO_NOTHING,
        related_query_name="+",
        help_text="Race of the player character.",
        verbose_name="Race",
    )
    total_renown = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total renown the player earned in the season.",
        verbose_name="Total Renown",
    )
    challenges_completed = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of challenges the player completed in the season.",
        verbose_name="Challenges Completed",
    )
    quests_completed = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of quests the player completed in the season.",
        verbose_name="Quests Completed",
    )
    deaths = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of times the player died in the season.",
        verbose_name="Deaths",
    )
    game_type = models.IntegerField(
        blank=True,
        null=True,
        choices=GameType,
        help_text="Game type of the player character (classic/hardcore/survival).",
        verbose_name="Game Type",
    )
    play_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Seconds the player spent in-game during the season.",
        verbose_name="Play Time",
    )
    level = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Level the player finished the season at.",
        verbose_name="Level",
    )

    class Meta:
        managed = False
        db_table = "historic_season_stat"
        ordering = ("-season_id", "-remorts")
        verbose_name = "Historic Season Stat"
        verbose_name_plural = "Historic Season Stats"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.player_name} @ Season {self.season_id}"
