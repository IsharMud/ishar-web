"""Fated essence, mirrored from the game (ishar-mud ``tension_essence.h``,
``tension_essence.c`` and ``tally_fated_essence`` in ``tension.c``; the loose
rule of ishar-mud#1990). Integer math, division last. Deliberately free of
Django so the payout tables can be pinned without a database.

The account stores what pays: ``season_woven_essence`` (banked by ascension)
and ``season_loose_essence`` (the season's high-water across lives). Those are
displayed as stored, never recomputed; the formulas here only price the life
in hand and what its further remorts and its ascension would do.
"""
from dataclasses import dataclass


SLOPE_PCT = 20      # each Tension point adds 20% to a life's multiplier
SUMMIT = 10         # remorts a life can hold; the eleventh prayer ascends
BANK_BASE = 16      # woven essence an ascension banks at Tension 0

PLAYED_BONUS = 2    # for having played a Fated this season
CLIMB_BONUS = 1     # for holding any woven or loose essence


def multiply(value: int, tension: int) -> int:
    """value x (100 + 20T) / 100."""
    return int(value) * (100 + SLOPE_PCT * max(0, int(tension))) // 100


def loose_value(remorts: int, tension: int) -> int:
    """What a life standing at ``remorts`` under net Tension T is worth."""
    return multiply(min(max(0, int(remorts)), SUMMIT), tension)


def bank(tension: int) -> int:
    """Woven essence the eleventh prayer banks at net Tension T."""
    return multiply(BANK_BASE, tension)


def rules() -> dict:
    """The constants the web client's HUD prices a life with."""
    return {"slope_pct": SLOPE_PCT, "summit": SUMMIT, "bank_base": BANK_BASE}


def season_total(woven: int, loose: int, played: bool, milestones: int) -> int:
    climb = woven + loose
    total = climb + milestones
    if played or climb > 0:
        total += PLAYED_BONUS
    if climb > 0:
        total += CLIMB_BONUS
    return total


@dataclass(frozen=True)
class Step:
    """One further remort of the life in hand."""

    remorts: int
    worth: int
    loose: int          # the season's loose essence once this remort is made
    total: int
    passes: bool        # the first remort to rise above the stored high-water


@dataclass(frozen=True)
class Ascension:
    tension: int
    bank: int
    loose_replaced: int     # loose the life would hold at the summit
    total_before: int       # season total at the summit
    total_after: int

    @property
    def change(self) -> int:
        return self.total_after - self.total_before

    @property
    def change_display(self) -> str:
        return f"{self.change:+d}".replace("-", "\u2212") if self.change else "\u00b10"


@dataclass(frozen=True)
class SeasonEssence:
    """An account's essence this season, plus the life in hand priced
    remort by remort. ``life_remorts`` is None when no Fated life is under
    way; ``life_tension`` -1 (knots untied) reckons as Tension 0."""

    woven: int
    loose: int
    loose_remorts: int
    loose_tension: int
    played: bool
    milestones: int
    life_remorts: int | None = None
    life_tension: int = 0
    life_name: str = ""

    @property
    def total(self) -> int:
        return season_total(self.woven, self.loose, self.played, self.milestones)

    @property
    def played_bonus(self) -> int:
        return PLAYED_BONUS if self.played or self.woven + self.loose > 0 else 0

    @property
    def climb_bonus(self) -> int:
        return CLIMB_BONUS if self.woven + self.loose > 0 else 0

    @property
    def sourced(self) -> bool:
        """The game records the life that set the high-water; remorts 0
        means it was set before the pair was kept, under the earlier rule."""
        return self.loose_remorts > 0

    @property
    def earlier_rule(self) -> bool:
        return self.loose > 0 and not self.sourced

    @property
    def has_life(self) -> bool:
        return self.life_remorts is not None

    @property
    def life_untied(self) -> bool:
        return self.has_life and self.life_tension < 0

    @property
    def tension(self) -> int:
        return max(0, self.life_tension)

    @property
    def multiplier_display(self) -> str:
        """The life's multiplier as a factor: Tension 19 -> '×4.8'."""
        pct = 100 + SLOPE_PCT * self.tension
        whole, frac = divmod(pct, 100)
        return f"\u00d7{whole}" + (f".{frac:02d}".rstrip("0") if frac else "")

    @property
    def summit(self) -> int:
        return SUMMIT

    @property
    def at_summit(self) -> bool:
        return self.has_life and self.life_remorts >= SUMMIT

    @property
    def life_worth(self) -> int | None:
        if not self.has_life:
            return None
        return loose_value(self.life_remorts, self.tension)

    @property
    def below_high_water(self) -> bool:
        return self.has_life and self.life_worth < self.loose

    def _total_with_loose(self, loose: int) -> int:
        return season_total(self.woven, loose, self.played, self.milestones)

    @property
    def steps(self) -> list[Step]:
        if not self.has_life:
            return []
        steps, passed = [], self.life_worth > self.loose
        for remorts in range(self.life_remorts + 1, SUMMIT + 1):
            worth = loose_value(remorts, self.tension)
            loose = max(self.loose, worth)
            passes = not passed and worth > self.loose
            passed = passed or passes
            steps.append(Step(remorts, worth, loose, self._total_with_loose(loose), passes))
        return steps

    @property
    def passes_at(self) -> Step | None:
        return next((s for s in self.steps if s.passes), None)

    @property
    def ascension(self) -> Ascension | None:
        if not self.has_life:
            return None
        banked = bank(self.tension)
        at_summit = max(self.loose, loose_value(SUMMIT, self.tension))
        return Ascension(
            tension=self.tension,
            bank=banked,
            loose_replaced=at_summit,
            total_before=self._total_with_loose(at_summit),
            total_after=season_total(self.woven + banked, 0, self.played, self.milestones),
        )
