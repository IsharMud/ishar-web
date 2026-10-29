"""Template context for the Tension panels, shared by the player profile and
the portal so both pages read the same numbers from the same code."""
from apps.seasons.utils import get_current_season

from .tension import HELP_TOPICS, account_loom, account_standing, burden_table, player_life


def fated_season_active() -> bool:
    try:
        season = get_current_season()
    except Exception:
        return False
    return bool(season and season.is_fated)


def account_tension_context(account, in_fated_season=None) -> dict:
    """The account-level Tension block: standing + the loom. Empty outside a
    Fated season, where every season field reads as zero."""
    if in_fated_season is None:
        in_fated_season = fated_season_active()
    if not in_fated_season:
        return {}
    return {
        "standing": account_standing(account),
        "loom": account_loom(account),
        "help_topics": HELP_TOPICS,
        "burden_table": burden_table(),
    }


def player_tension_context(player, in_fated_season=None) -> dict:
    """The character-level block (this life) plus the account block. Empty for
    a non-Fated character."""
    if not player.is_fated():
        return {}
    context = account_tension_context(player.account, in_fated_season)
    if not context:
        return {}
    context["life"] = player_life(player, loom=context["loom"])
    context["between_lives"] = bool(player.is_deleted)
    return context
