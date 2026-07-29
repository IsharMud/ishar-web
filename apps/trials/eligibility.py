"""
Soft eligibility check for the Immortal Trial: the policy asks for at least
one full season played and two remorts. Displayed to the applicant and to
reviewers as guidance — never enforced, so staff can waive edge cases.
"""
from dataclasses import dataclass

from django.db import DatabaseError
from django.db.models import Case, Count, F, IntegerField, Max, When
from django.db.models.functions import Coalesce

MIN_SEASONS = 1
MIN_REMORTS = 2


@dataclass(frozen=True)
class Eligibility:
    seasons_played: int
    best_remorts: int

    @property
    def meets_seasons(self) -> bool:
        return self.seasons_played >= MIN_SEASONS

    @property
    def meets_remorts(self) -> bool:
        return self.best_remorts >= MIN_REMORTS

    @property
    def eligible(self) -> bool:
        return self.meets_seasons and self.meets_remorts

    def as_payload(self) -> dict:
        """Numbers for the Discord outbox payload."""
        return {
            "eligible": self.eligible,
            "seasons": self.seasons_played,
            "remorts": self.best_remorts,
        }


def check(account) -> Eligibility:
    """
    Compute eligibility from mortal characters (current season) and
    `historic_season_stat` snapshots (a row only exists once `cycle_season`
    has archived a completed season, so distinct seasons there == full
    seasons played).
    """
    from apps.players.models.game_type import GameType
    from apps.players.models.player import Player
    from apps.seasons.models.historic import HistoricSeasonStat

    try:
        # Rank hardcore characters by their permadeath-proof record — the
        # same Coalesce the leaderboard uses (apps/leaders/views.py).
        current = Player.objects.filter(account=account).aggregate(
            best=Max(Case(
                When(
                    game_type=GameType.HARDCORE,
                    then=Coalesce("statistics__hardcore_remorts", "remorts"),
                ),
                default=F("remorts"),
                output_field=IntegerField(),
            )),
        )["best"] or 0
        historic = HistoricSeasonStat.objects.filter(account=account).aggregate(
            seasons=Count("season", distinct=True),
            best=Max("remorts"),
        )
        return Eligibility(
            seasons_played=historic["seasons"] or 0,
            best_remorts=max(current, historic["best"] or 0),
        )
    except DatabaseError:
        return Eligibility(seasons_played=0, best_remorts=0)
