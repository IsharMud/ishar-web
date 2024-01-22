"""
Ishar MUD API configuration.
"""
from django.conf import settings
from ninja import NinjaAPI
from ninja.security import django_auth_superuser, HttpBearer


def local_debug(request):
    if (
        settings.DEBUG and settings.ALLOWED_HOSTS[0] == "127.0.0.1" and
        request.META["REMOTE_ADDR"] == "127.0.0.1"
    ):
        return True
    return False


class BearerToken(HttpBearer):
    def authenticate(self, request, token):
        if token == settings.REST_TOKEN:
            return True
        return False


api = NinjaAPI(
    auth=(local_debug, BearerToken(), django_auth_superuser),
    csrf=False,
    description=f"{settings.WEBSITE_TITLE} API",
    docs_url="/",
    title=settings.WEBSITE_TITLE,
    version="4.6.0"
)

from ishar.apps.accounts.api import accounts, account_id, account_name
from ishar.apps.accounts.api.players import (
    account_id_players, account_name_players
)
from ishar.apps.accounts.api.upgrades import (
    upgrades, account_id_upgrades, account_name_upgrades
)

from ishar.apps.challenges.api import (
    challenges, active, complete, inactive, incomplete, challenge
)
from ishar.apps.patches.api import patches, latest, hidden, visible, patch

from ishar.apps.players.api import players, player_id, player_name
from ishar.apps.players.api.classic import classic
from ishar.apps.players.api.survival import survival, dead, living
from ishar.apps.players.api.immortals import immortals
from ishar.apps.players.api.who import who

from ishar.apps.seasons.api import current, seasons, season
