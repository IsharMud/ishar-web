"""
Ishar MUD API configuration.
"""
from django.conf import settings
from ninja import NinjaAPI
from ninja.security import django_auth_superuser


def local_debug(request):
    if (
        settings.DEBUG and settings.ALLOWED_HOSTS[0] == "127.0.0.1" and
        request.META["REMOTE_ADDR"] == "127.0.0.1"
    ):
        return True
    return False


api = NinjaAPI(
    auth=(local_debug, django_auth_superuser),
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
from ishar.apps.players.api import (
    players, player_id, player_name, classic, survival, dead, living, immortals
)
from ishar.apps.seasons.api import current, seasons, season
