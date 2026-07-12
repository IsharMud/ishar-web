"""Shared staff-attribution helper (used by feedback triage and the admin
consoles' `web_admin_queue` rows)."""
import logging


log = logging.getLogger(__name__)


def staff_name(account) -> str:
    """
    Best display name for a staff member's actions, matching the in-game
    attribution (character name). Falls back to the account login name.
    """
    try:
        immortal = account.players.order_by("-true_level").first()
        if immortal and immortal.name:
            return str(immortal.name)
    except Exception:  # pragma: no cover - defensive; never block an action
        log.warning("staff: could not resolve immortal name for %s", account)
    return account.get_username()
