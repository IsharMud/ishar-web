from typing import List

from django.conf import settings
from django.shortcuts import get_object_or_404

from ishar.apps.core.api import api
from ishar.apps.players.models.player import Player
from ishar.apps.players.api.schemas import PlayerSchema


@api.get(
    path="/players/",
    response=List[PlayerSchema],
    summary="All players (except immortals).",
    tags=["players"]
)
def players(request):
    """All players - excluding Immortals, Artisans, Eternals, Gods, etc."""
    return Player.objects.exclude(
        true_level__gte=settings.MIN_IMMORTAL_LEVEL
    ).all()


@api.get(
    path="/player/id/{id}/",
    response=PlayerSchema,
    summary="Single player, by ID.",
    tags=["players"]
)
def player_id(request, id: int):
    """Player, by ID."""
    return get_object_or_404(Player, id=id)


@api.get(
    path="/player/name/{name}/",
    response=PlayerSchema,
    summary="Single player, by name.",
    tags=["players"]
)
def player_name(request, name: str):
    """Player, by name."""
    return get_object_or_404(Player, name=name)
