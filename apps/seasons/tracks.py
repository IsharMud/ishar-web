"""Engagement track reads and pre-flight validation for the track console.

The game owns `engagement_tracks` and is the authority on what a valid track
is (`rust-interop/src/engagement_track.rs`). The bounds here mirror it only so
an operator gets an immediate, specific message instead of waiting a game
minute for a rejection; when the two disagree, the game wins and its result
string is what the console shows.
"""
from django.db import DatabaseError, connection

from apps.core.models.title import Title
from apps.objects.models.object import Object

from .models.track import EngagementTrack, TrackScope


MAX_MILESTONES = 12
MAX_REWARDS_PER_MILESTONE = 4
CAP_BPS = 10_000
MAX_LOOT_BOX_COUNT = 10

STANDARD_SEASON_MONTHS = 4
SEASON_MONTHS_RANGE = range(1, 13)

# kind -> (label, value label, max per reward, max summed over the track)
REWARD_KINDS = {
    "xp_buff_percent": ("Passive XP bonus", "Percent", 25, 25),
    "shop_discount_percent": ("Passive shop discount", "Percent", 50, 50),
    "renown": ("Renown", "Amount", 500, 1000),
    "essence": ("Essence", "Amount", 5, 10),
    "loot_box": ("Loot box", "Object vnum", None, None),
    "memory": ("Memory", "Object vnum", None, None),
    "title": ("Title", "Title", None, None),
}
OBJECT_KINDS = ("loot_box", "memory")

# The console's scope names. `current` is resolved to the active season by
# the game, so a save queued across a cycle can never land on a stale id.
EDITABLE_SCOPES = ("current", "upcoming", "standard")
REVERTIBLE_SCOPES = ("current", "upcoming")


class TrackError(ValueError):
    """A track the game would reject; the message is shown to the operator."""


def _whole(value, what: str, low: int, high: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TrackError(f"{what} must be a whole number.")
    if value < low or (high is not None and value > high):
        bound = f"{low}-{high}" if high is not None else f"at least {low}"
        raise TrackError(f"{what} must be {bound}.")
    return value


def _clean_reward(raw, where: str) -> dict:
    if not isinstance(raw, dict):
        raise TrackError(f"{where}: malformed reward.")
    kind = raw.get("kind")
    if kind not in REWARD_KINDS:
        raise TrackError(f"{where}: unknown reward kind.")
    label, _, per_reward_max, _ = REWARD_KINDS[kind]
    reward = {
        "kind": kind,
        "value": _whole(raw.get("value"), f"{where}: {label}", 1, per_reward_max),
    }
    if kind == "loot_box":
        reward["count"] = _whole(
            raw.get("count", 1), f"{where}: loot box count", 1, MAX_LOOT_BOX_COUNT
        )
    return reward


def clean_milestones(raw) -> list[dict]:
    """Validate editor output into the payload shape the game expects.

    Milestones the editor added carry no `slot`; the game assigns one.
    """
    if not isinstance(raw, list) or not 1 <= len(raw) <= MAX_MILESTONES:
        raise TrackError(f"A track needs 1-{MAX_MILESTONES} milestones.")

    milestones, slots, previous = [], set(), 0
    totals = dict.fromkeys(REWARD_KINDS, 0)
    for number, item in enumerate(raw, start=1):
        where = f"Milestone {number}"
        if not isinstance(item, dict):
            raise TrackError(f"{where}: malformed milestone.")
        at_bps = _whole(item.get("at_bps"), f"{where}: threshold", 1, CAP_BPS)
        if at_bps <= previous:
            raise TrackError(f"{where}: threshold must be above the one before it.")
        previous = at_bps

        rewards = item.get("rewards")
        if (
            not isinstance(rewards, list)
            or not 1 <= len(rewards) <= MAX_REWARDS_PER_MILESTONE
        ):
            raise TrackError(
                f"{where}: needs 1-{MAX_REWARDS_PER_MILESTONE} rewards."
            )
        milestone = {
            "at_bps": at_bps,
            "rewards": [_clean_reward(reward, where) for reward in rewards],
        }
        for reward in milestone["rewards"]:
            totals[reward["kind"]] += reward["value"]

        slot = item.get("slot")
        if slot is not None:
            slot = _whole(slot, f"{where}: slot", 0, 65_535)
            if slot in slots:
                raise TrackError(f"{where}: slot {slot} is used twice.")
            slots.add(slot)
            milestone = {"slot": slot, **milestone}
        milestones.append(milestone)

    if previous != CAP_BPS:
        raise TrackError("The last milestone must sit at 100%.")
    for kind, (label, _, _, track_max) in REWARD_KINDS.items():
        if track_max is not None and totals[kind] > track_max:
            raise TrackError(
                f"Total {label.lower()} across the track is {totals[kind]};"
                f" the limit is {track_max}."
            )

    _check_references(milestones)
    return milestones


def _check_references(milestones: list[dict]) -> None:
    rewards = [r for m in milestones for r in m["rewards"]]
    title_ids = {r["value"] for r in rewards if r["kind"] == "title"}
    vnums = {r["value"] for r in rewards if r["kind"] in OBJECT_KINDS}
    missing_titles = title_ids - set(
        Title.objects.filter(title_id__in=title_ids).values_list("title_id", flat=True)
    )
    if missing_titles:
        raise TrackError(f"Title {min(missing_titles)} does not exist.")
    missing_objects = vnums - set(
        Object.objects.filter(vnum__in=vnums).values_list("vnum", flat=True)
    )
    if missing_objects:
        raise TrackError(f"Object {min(missing_objects)} does not exist.")


def object_name(vnum: int) -> str | None:
    found = Object.objects.filter(vnum=vnum).first()
    return str(found) if found else None


def claim_counts(season_id: int) -> dict[int, int]:
    """Accounts that have claimed each milestone slot this season."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT milestone, COUNT(*) FROM accounts_engagement_rewards"
            " WHERE season_id = %s GROUP BY milestone",
            [season_id],
        )
        return {int(slot): int(count) for slot, count in cursor.fetchall()}


def claimed_milestones(account_id: int, season_id: int) -> int:
    """Milestones an account has claimed this season. The game pays one
    essence per milestone *reached*, which it derives on read and never
    stores, so a reached-but-unclaimed milestone is missing here: this is a
    lower bound on the engagement essence."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(DISTINCT milestone) FROM accounts_engagement_rewards"
            " WHERE account_id = %s AND season_id = %s",
            [account_id, season_id],
        )
        return int(cursor.fetchone()[0])


def console_state(season) -> dict | None:
    """Everything the track console's editor needs, or None when the game's
    `engagement_tracks` migration has not run yet."""
    try:
        rows = list(EngagementTrack.objects.all())
        claims = claim_counts(season.season_id)
    except DatabaseError:
        return None

    def find(scope, season_id=0):
        return next(
            (r for r in rows if r.scope == scope and r.season_id == season_id), None
        )

    standard = find(TrackScope.STANDARD)
    if standard is None:
        return None

    def scope_state(label, row, live):
        source = row or standard
        return {
            "label": label,
            "custom": row is not None,
            "live": live,
            "milestones": source.milestones,
            "updated_by": source.updated_by,
            "updated_at": source.updated_at.isoformat(),
        }

    current = find(TrackScope.SEASON, season.season_id)
    scopes = {
        "current": scope_state(f"Season {season.season_id}", current, True),
        "upcoming": scope_state("Next season", find(TrackScope.UPCOMING), False),
        # Editing the template changes the live track only while the current
        # season is inheriting it.
        "standard": scope_state("Standard template", standard, current is None),
    }
    scopes["standard"]["custom"] = False

    vnums = {
        reward["value"]
        for scope in scopes.values()
        for milestone in scope["milestones"]
        for reward in milestone["rewards"]
        if reward["kind"] in OBJECT_KINDS
    }
    return {
        "scopes": scopes,
        "claims": claims,
        "kinds": [
            {
                "kind": kind,
                "label": label,
                "value_label": value_label,
                "max": per_reward_max,
            }
            for kind, (label, value_label, per_reward_max, _) in REWARD_KINDS.items()
        ],
        "titles": [
            {"id": title.title_id, "name": str(title)} for title in Title.objects.all()
        ],
        "objects": {
            obj.vnum: str(obj) for obj in Object.objects.filter(vnum__in=vnums)
        },
        "limits": {
            "milestones": MAX_MILESTONES,
            "rewards": MAX_REWARDS_PER_MILESTONE,
            "loot_box_count": MAX_LOOT_BOX_COUNT,
        },
    }


def next_season_length(season) -> dict | None:
    """The next season's length: the going-live enigma's default and any
    one-cycle override. None when the game's `next_duration_months` migration
    has not run. Read raw and guarded: the column is deliberately not on the
    `Season` model, so a site deployed ahead of the game migration still
    serves every season page."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT next_duration_months FROM seasons WHERE season_id = %s",
                [season.season_id],
            )
            row = cursor.fetchone()
    except DatabaseError:
        return None
    enigma = season.next_enigma
    default = enigma.season_duration_months if enigma else STANDARD_SEASON_MONTHS
    override = row[0] if row else None
    return {
        "default": default,
        "override": override,
        "effective": override or default,
    }
