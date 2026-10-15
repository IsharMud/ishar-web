"""Tension arithmetic, mirrored from the game (ishar-mud ``dbase/tension.c``,
``docs/fated_tension_spec.md``). Integer math throughout; weights and burden
are integer tenths. ``players.tension_locked`` is the authoritative value for
a life — these helpers exist for display breakdowns and account panels.
"""
from dataclasses import dataclass, field

from apps.skills.utils import PASSIVE_SKILL_TYPE, RARITY_NAMES

from .models import AccountFatedSkill, TensionModifier


FATED_CLASS_ID = 17            # player_common.class_id of the Fated class
FATED_ENIGMA_ID = 2            # seasonal_enigma_id of Fractured Threads
SUMMIT_REMORTS = 10            # the prayer after the summit ascends
MULT_SLOPE_PCT = 20            # m(T) = (100 + 20T) / 100
KNOTS_UNTIED = -1              # players.tension_locked before the knots are tied

RARITY_BURDEN = (2, 3, 5, 10, 15)   # tenths per bind, by rarity index

HELP_TOPICS = ("Tension", "Knots", "Ascension", "Woven")


def tenths(value) -> str:
    """Render integer tenths as one decimal: 20 -> '2.0', 5 -> '0.5'."""
    value = int(value or 0)
    sign = "-" if value < 0 else ""
    return f"{sign}{abs(value) // 10}.{abs(value) % 10}"


def essence_formula(remorts: int) -> int:
    """f(r) = r + (r/5)*3 — the per-character essence formula."""
    remorts = max(0, int(remorts))
    return remorts + (remorts // 5) * 3


def multiply(value: int, tension: int) -> int:
    """value × m(T), integer division last."""
    return value * (100 + MULT_SLOPE_PCT * max(0, int(tension))) // 100


def bank(tension: int) -> int:
    """Woven essence an ascension banks at net Tension T: f(10) × m(T)."""
    return multiply(essence_formula(SUMMIT_REMORTS), tension)


def rarity_name(rarity) -> str:
    rarity = int(rarity or 0)
    return RARITY_NAMES[min(max(rarity, 0), len(RARITY_NAMES) - 1)]


def thread_burden(rarity, skill_type, skill_level) -> int:
    """Burden of one bound thread in tenths: rarity-priced, per tier for a
    passive, nothing for a severed thread."""
    if int(skill_level or 0) == AccountFatedSkill.SEVERED:
        return 0
    rarity = min(max(int(rarity or 0), 0), len(RARITY_BURDEN) - 1)
    per_bind = RARITY_BURDEN[rarity]
    if int(skill_type or 0) == PASSIVE_SKILL_TYPE:
        return per_bind * max(1, int(skill_level or 0))
    return per_bind


def net_tension(knot_weight: int, burden: int) -> int:
    """(knot weight − burden) floored at 0, in whole points."""
    return max(0, int(knot_weight) - int(burden)) // 10


@dataclass
class Thread:
    skill_id: int
    name: str
    level: int
    rarity: int
    rarity_name: str
    burden: int                      # tenths
    severed: bool
    passive: bool

    @property
    def burden_display(self) -> str:
        return tenths(self.burden)


@dataclass
class Knot:
    modifier: TensionModifier
    tied: bool = False

    @property
    def name(self) -> str:
        return self.modifier.name

    @property
    def rule(self) -> str:
        return self.modifier.description

    @property
    def weight(self) -> int:
        return self.modifier.weight

    @property
    def weight_display(self) -> str:
        return tenths(self.modifier.weight)


@dataclass
class Loom:
    """An account's bound pool, priced."""

    threads: list = field(default_factory=list)

    @property
    def bound(self) -> list:
        return [t for t in self.threads if not t.severed]

    @property
    def severed(self) -> list:
        return [t for t in self.threads if t.severed]

    @property
    def burden(self) -> int:
        return sum(t.burden for t in self.threads)

    @property
    def burden_display(self) -> str:
        return tenths(self.burden)


def account_loom(account) -> Loom:
    """The account's pool, thread by thread, severed threads included
    (weightless) so the view can strike them through."""
    rows = (
        AccountFatedSkill.objects.filter(account=account)
        .select_related("skill")
        .order_by("skill__skill_name")
    )
    threads = []
    for row in rows:
        skill = row.skill
        threads.append(Thread(
            skill_id=skill.pk,
            name=skill.skill_name or skill.enum_symbol,
            level=row.skill_level,
            rarity=skill.rarity or 0,
            rarity_name=rarity_name(skill.rarity),
            burden=thread_burden(skill.rarity, skill.skill_type, row.skill_level),
            severed=row.is_severed,
            passive=skill.skill_type == PASSIVE_SKILL_TYPE,
        ))
    return Loom(threads=threads)


def knot_menu() -> list:
    """Every knot on the loom's menu, family by family, tiers ascending."""
    return list(TensionModifier.objects.all())


def tied_knots(mask: int, menu=None) -> list:
    """Knots a life has tied, in menu order. A corrupt mask holding two tiers
    of one family resolves to the top tier, as the game does."""
    mask = int(mask or 0)
    by_family = {}
    for knot in (menu if menu is not None else knot_menu()):
        if mask & knot.bit:
            current = by_family.get(knot.family)
            if current is None or knot.tier > current.tier:
                by_family[knot.family] = knot
    return [Knot(modifier=k, tied=True) for k in by_family.values()]


def knot_weight(knots) -> int:
    return sum(k.weight for k in knots)


@dataclass
class Life:
    """This life's Tension, as the `score` line reads it."""

    locked: int                      # players.tension_locked
    remorts: int
    knots: list
    burden: int                      # tenths, live
    summit: int = SUMMIT_REMORTS

    @property
    def untied(self) -> bool:
        return self.locked == KNOTS_UNTIED

    @property
    def tension(self) -> int:
        return max(0, self.locked)

    @property
    def knot_weight(self) -> int:
        return knot_weight(self.knots)

    @property
    def knot_weight_display(self) -> str:
        return tenths(self.knot_weight)

    @property
    def burden_display(self) -> str:
        return tenths(self.burden)

    @property
    def at_summit(self) -> bool:
        return self.remorts >= self.summit

    @property
    def bank(self) -> int:
        return bank(self.tension)


def player_life(player, loom=None) -> Life:
    loom = loom if loom is not None else account_loom(player.account)
    return Life(
        locked=player.tension_locked,
        remorts=player.remorts,
        knots=tied_knots(player.knots_mask),
        burden=loom.burden,
    )


@dataclass
class Standing:
    """An account's season and lifetime Tension standing."""

    woven: int
    loose: int
    best: int
    lifetime_best: int

    @property
    def this_season(self) -> int:
        return self.woven + self.loose

    @property
    def any(self) -> bool:
        return bool(self.woven or self.loose or self.best or self.lifetime_best)


def account_standing(account) -> Standing:
    return Standing(
        woven=account.season_woven_essence or 0,
        loose=account.season_loose_essence or 0,
        best=account.season_max_tension or 0,
        lifetime_best=account.max_tension or 0,
    )
