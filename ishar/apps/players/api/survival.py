from typing import List

from django.conf import settings

from ishar.api import api
from ishar.apps.players.models import GameType, Player
from ishar.apps.players.api.schemas import PlayerSchema


@api.get(
    path="/players/hardcore/",
    response=List[PlayerSchema],
    summary="Hardcore players.",
    tags=["players"]
)
def hardcore(request):
    """Hardcore players."""
    return Player.objects.filter(
        true_level__lt=settings.MIN_IMMORTAL_LEVEL,
        game_type__exact=GameType.HARDCORE
    ).all()


@api.get(
    path="/players/survival/",
    response=List[PlayerSchema],
    summary="Survival players.",
    tags=["players"]
)
def survival(request):
    """Survival players."""
    return Player.objects.filter(
        true_level__lt=settings.MIN_IMMORTAL_LEVEL,
        game_type__exact=GameType.SURVIVAL
    ).all()


@api.get(
    path="/players/dead/",
    response=List[PlayerSchema],
    summary="Dead players.",
    tags=["players"]
)
def dead(request):
    """Dead players."""
    return Player.objects.filter(
        true_level__lt=settings.MIN_IMMORTAL_LEVEL,
        game_type__gt=GameType.CLASSIC,
        is_deleted__exact=1
    ).all()


@api.get(
    path="/players/living/",
    response=List[PlayerSchema],
    summary="Living players.",
    tags=["players"]
)
def living(request):
    """Living players."""
    return Player.objects.filter(
        true_level__lt=settings.MIN_IMMORTAL_LEVEL,
        game_type__gt=GameType.CLASSIC,
        is_deleted__exact=0
    ).all()
