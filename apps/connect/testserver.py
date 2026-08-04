"""Test-server (staging) access policy for ``/connect``.

The staging game is the authority on who may actually log in — its login
gates admit beta testers during closed beta and staff only while beta is
off (ishar-mud, ``server.c``). This module mirrors that policy web-side so
the page can offer, hide, or refuse the test option *before* dialing, keyed
off the staging season's persisted ``game_state`` (set in-game with
``admin beta <open|closed|off>``, saved by ``save_season()``).

Tiers:

* **Open beta** — every signed-in account.
* **Closed beta** — accounts flagged ``beta_tester``, plus staff.
* **Beta off** (or the staging DB unreachable) — staff only. Failing closed
  costs nothing: the game refuses non-staff logins in those states anyway.

"Staff" here is Artisan+ (``is_artisan``), matching the game gate's
``IMM_ARTISAN`` floor exactly — the two policies must not drift.

Deliberate web/telnet difference: the raw staging telnet port still admits
anonymous visitors during open beta, but ``/connect`` requires a portal
login for every session, test included.
"""
import logging

from django.conf import settings
from django.core.cache import cache

from apps.seasons.models.season import GameState


logger = logging.getLogger(__name__)

# The staging DB is an internet hop that backs both page renders and every
# websocket connect — cache the state briefly, including "unreachable" so a
# down box doesn't cost a connect timeout per request. The cache means the
# policy trails `admin beta` by up to 60s; that's advisory-tier only, since
# the game re-gates every login itself.
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
        if state is None:
            # Reachable but no active season — a mis-refreshed staging DB,
            # not a down box. Same fail-closed result, different fix.
            logger.warning("Staging DB reachable but no active season row")
    except Exception as exc:
        logger.warning("Staging game_state lookup failed: %s", exc)
        state = None
    cache.set(
        _CACHE_KEY, _UNREACHABLE if state is None else state, _CACHE_SECONDS
    )
    return state


def tier() -> str:
    """The current access tier: ``open``, ``closed``, or ``staff``."""
    state = staging_game_state()
    if state == GameState.OPEN_BETA:
        return "open"
    if state == GameState.CLOSED_BETA:
        return "closed"
    return "staff"


def allowed(user) -> bool:
    """Whether this user may open a test-server session right now."""
    if not enabled():
        return False
    if not getattr(user, "is_authenticated", False):
        return False
    current = tier()
    if current == "open":
        return True
    if user.is_artisan():
        return True
    return current == "closed" and bool(user.beta_tester)


# Login-identity columns refreshed on every test connect. The rest of the
# row is seeded once and then belongs to staging — gameplay writes stay
# local, and players/characters are never synced.
_IDENTITY_FIELDS = ("password", "beta_tester", "immortal_level", "banned_until")


def sync_account(email: str) -> int:
    """Seed or refresh this prod account on staging; return its staging id.

    The unified-account model: one login identity everywhere, separate
    character sets. The first test connect copies the whole prod accounts
    row (fresh characters; the referrer id is nulled — it points into
    prod's id space); after that only the identity columns track prod, so
    a password change or beta revocation reaches staging the next time the
    player web-connects. Raises on any failure — including a unique-key
    collision with a stale staging row after a prod email change, which
    needs a re-dump or admin cleanup — and the caller degrades to manual
    login.
    """
    from apps.accounts.models import Account

    prod = Account.objects.get(email=email)
    staging_id = (
        Account.objects.using("staging")
        .filter(email=email)
        .values_list("account_id", flat=True)
        .first()
    )
    if staging_id is not None:
        Account.objects.using("staging").filter(account_id=staging_id).update(
            **{f: getattr(prod, f) for f in _IDENTITY_FIELDS}
        )
        return staging_id

    values = {
        f.attname: getattr(prod, f.attname)
        for f in Account._meta.concrete_fields
        if not f.primary_key
    }
    values["referrer_account_id"] = None
    return Account.objects.using("staging").create(**values).account_id
