"""Template context for the Tension panels, shared by the player profile and
the portal so both pages read the same numbers from the same code."""
from django.db import DatabaseError

from apps.players.models import Player
from apps.seasons.tracks import claimed_milestones
from apps.seasons.utils import get_current_season

from .essence import SeasonEssence
from .tension import (
    FATED_CLASS_ID, HELP_TOPICS, account_loom, account_standing, burden_table,
    player_life,
)


def current_fated_season():
    """The current season when it is a Fated one, else None."""
    try:
        season = get_current_season()
    except Exception:
        return None
    return season if season and season.is_fated else None


def fated_season_active() -> bool:
    return current_fated_season() is not None


def season_essence(account, season, life=None) -> SeasonEssence:
    """The account's essence this season, as the game tallies it, with
    ``life`` (a living Fated character, or None) priced remort by remort.
    Every mortal Fated row counts as having played, alive or not — the
    game's tally asks the same question."""
    try:
        milestones = claimed_milestones(account.pk, season.season_id)
    except DatabaseError:
        milestones = 0
    return SeasonEssence(
        woven=account.season_woven_essence or 0,
        loose=account.season_loose_essence or 0,
        loose_remorts=account.season_loose_remorts or 0,
        loose_tension=account.season_loose_tension or 0,
        played=Player.objects.filter(
            account=account, common__player_class_id=FATED_CLASS_ID,
        ).exists(),
        milestones=milestones,
        life_remorts=life.remorts if life is not None else None,
        life_tension=life.tension_locked if life is not None else 0,
        life_name=life.name.title() if life is not None else "",
    )


def living_fated(account):
    """The account's Fated character whose run is under way, if any."""
    return (
        Player.objects.filter(
            account=account, common__player_class_id=FATED_CLASS_ID, is_deleted=0,
        )
        .order_by("-logon")
        .first()
    )


def account_tension_context(account, life=None, season=None) -> dict:
    """The account-level block: season essence (``life`` priced, if any),
    standing and the loom. Empty outside a Fated season, where every season
    field reads as zero."""
    season = season or current_fated_season()
    if season is None:
        return {}
    return {
        "essence": season_essence(account, season, life),
        "standing": account_standing(account),
        "loom": account_loom(account),
        "help_topics": HELP_TOPICS,
        "burden_table": burden_table(),
    }


def portal_tension_context(account) -> dict:
    """The portal prices the account's living Fated character."""
    season = current_fated_season()
    if season is None:
        return {}
    return account_tension_context(account, living_fated(account), season)


def player_tension_context(player) -> dict:
    """The character-level block (this life) plus the account block, with
    this character as the life priced. Empty for a non-Fated character."""
    if not player.is_fated():
        return {}
    between_lives = bool(player.is_deleted)
    context = account_tension_context(player.account, None if between_lives else player)
    if not context:
        return {}
    context["life"] = player_life(player, loom=context["loom"])
    context["between_lives"] = between_lives
    return context
