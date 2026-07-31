"""Test-server (staging) access policy for ``/connect``.

The staging game is the authority on who may actually log in — its login
gates admit beta testers during closed beta and staff only while beta is
off (ishar-mud, ``server.c``). This module mirrors that policy web-side so
the page can offer, hide, or refuse the test option *before* dialing, keyed
off the staging season's persisted ``game_state`` (set in-game with
``admin beta <open|closed|off>``, saved by ``save_season()``).

Tiers:

* **Open beta** — everyone, guests included.
* **Closed beta** — accounts flagged ``beta_tester``, plus staff.
* **Beta off** (or the staging DB unreachable) — staff only. Failing closed
  costs nothing: the game refuses non-staff logins in those states anyway.
"""
import logging

from django.conf import settings
from django.core.cache import cache


logger = logging.getLogger(__name__)

# seasons.game_state values (ishar-mud src/include/constants.h, game_state_t).
GAME_STATE_OPEN_BETA = 3
GAME_STATE_CLOSED_BETA = 4

# The staging DB is an internet hop that backs both page renders and every
# websocket connect — cache the state briefly, including "unreachable" so a
# down box doesn't cost a 3s connect timeout per request.
_CACHE_KEY = "connect.test_server.game_state"
_CACHE_SECONDS = 60
_UNREACHABLE = "unreachable"


def enabled() -> bool:
    return bool(settings.MUD_TEST_HOST)


def staging_game_state():
    """The staging game's active-season ``game_state``; None if unreachable."""
    cached = cache.get(_CACHE_KEY)
    if cached is not None:
        return None if cached == _UNREACHABLE else cached

    from apps.seasons.models.season import Season

    try:
        state = (
            Season.objects.using("staging")
            .filter(is_active=1)
            .values_list("game_state", flat=True)
            .first()
        )
    except Exception as exc:
        logger.warning("Staging game_state lookup failed: %s", exc)
        state = None
    cache.set(
        _CACHE_KEY, _UNREACHABLE if state is None else state, _CACHE_SECONDS
    )
    return state


def allowed(user) -> bool:
    """Whether this user may open a test-server session right now."""
    if not enabled():
        return False
    state = staging_game_state()
    if state == GAME_STATE_OPEN_BETA:
        return True
    if not getattr(user, "is_authenticated", False):
        return False
    if user.is_eternal():
        return True
    return state == GAME_STATE_CLOSED_BETA and bool(user.beta_tester)
