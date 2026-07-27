"""JSON endpoint for the multiplay session picker (isharmud/ishar-web#178).

Feeds the "+ session" popover on ``/connect``: the account's characters,
which of them are already in-game, and the season's advisory multiplay
limit. Enforcement is the game's job (``check_multiplay()`` — immortals
bypass it entirely, mortals get the season limit); this payload only lets
the picker present honest choices before the game has its say.
"""
from datetime import timedelta

from django.conf import settings
from django.db import DatabaseError
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin
from apps.players.models.presence import GamePresence, PRESENCE_STALE_SECONDS
from apps.seasons.models import Season
from apps.seasons.utils.current import get_current_season

from .map import MapJSONMixin


class ConnectCharactersView(MapJSONMixin, NeverCacheMixin, View):
    """The account's characters and multiplay context (GET)."""

    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        cutoff = now() - timedelta(seconds=PRESENCE_STALE_SECONDS)
        try:
            online_ids = set(
                GamePresence.objects.filter(
                    account_id=request.user.account_id,
                    last_seen__gte=cutoff,
                ).values_list("player_id", flat=True)
            )
        except DatabaseError:
            online_ids = set()

        characters = [
            {
                "name": player.name,
                "level": player.true_level,
                "is_immortal": (
                    player.true_level >= settings.MIN_IMMORTAL_LEVEL
                ),
                "online": player.id in online_ids,
                "game_type": player.game_type,
            }
            for player in request.user.players.filter(
                is_deleted=False,
            ).order_by("-true_level", "name")
        ]

        try:
            multiplay_limit = get_current_season().multiplay_limit
        except (Season.DoesNotExist, DatabaseError):
            multiplay_limit = None

        return JsonResponse({
            "characters": characters,
            "multiplay_limit": multiplay_limit,
            "immortal_account": request.user.immortal_level > 0,
        })
