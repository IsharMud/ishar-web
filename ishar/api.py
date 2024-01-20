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

from ishar.apps.accounts.api import account, accounts, account_players
from ishar.apps.challenges.api import (
    challenge, challenges, complete, incomplete, active, inactive
)
from ishar.apps.players.api import (
    player, players, classic, survival, living, dead, immortals
)
from ishar.apps.seasons.api import current, season, seasons
