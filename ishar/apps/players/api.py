from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Schema
from typing import List

from ishar.api import api
from ishar.apps.players.models import Player


class PlayerAccountSchema(Schema):
    """Player account schema."""
    account_id: int
    account_name: str


class ImmortalSchema(Schema):
    """Immortal schema."""
    id: int
    name: str
    account: PlayerAccountSchema
    player_type: str


class PlayerSchema(Schema):
    """Player schema."""
    id: int
    name: str
    account: PlayerAccountSchema
    is_deleted: bool
    birth: datetime
    logon: datetime
    logout: datetime
    bankacc: int
    deaths: int
    remorts: int
    renown: int
    true_level: int
    favors: int
    total_renown: int
    quests_completed: int
    challenges_completed: int
    game_type: int
    player_stats: dict
    player_type: str


@api.get(
    path="/player/{name}/",
    response=PlayerSchema,
    tags=["players"]
)
def player(request, name: str):
    """Player, by name."""
    return get_object_or_404(Player, name=name)


@api.get(
    path="/players/",
    response=List[PlayerSchema],
    tags=["players"]
)
def players(request):
    """All players - excluding Immortals, Artisans, Eternals, Gods, etc."""
    return Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
    ).all()


@api.get(
    path="/players/classic/",
    response=List[PlayerSchema],
    tags=["players"]
)
def classic(request):
    """Classic players."""
    return Player.objects.filter(game_type__exact=0).all()


@api.get(
    path="/players/survival/",
    response=List[PlayerSchema],
    tags=["players"]
)
def survival(request):
    """Survival players."""
    return Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
        game_type__exact=1
    ).all()


@api.get(
    path="/players/survival/living/",
    response=List[PlayerSchema],
    tags=["players"]
)
def living(request):
    """Living survival players."""
    return Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
        game_type__exact=1,
        is_deleted__exact=0
    ).all()


@api.get(
    path="/players/survival/dead/",
    response=List[PlayerSchema],
    tags=["players"]
)
def dead(request):
    """Dead survival players."""
    return Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
        game_type__exact=1,
        is_deleted__exact=1
    ).all()


@api.get(path="/immortals/", response=List[ImmortalSchema], tags=["immortals"])
def immortals(request):
    """Immortals."""
    return Player.objects.filter(
        true_level__gte=min(settings.IMMORTAL_LEVELS)[0]
    ).all()
