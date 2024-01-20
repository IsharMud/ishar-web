from typing import List

from django.conf import settings

from ishar.api import api
from ishar.apps.players.models import Player
from ishar.apps.players.api.schemas import PlayerSchema


@api.get(
    path="/players/survival/",
    response=List[PlayerSchema],
    summary="Survival players.",
    tags=["players"]
)
def survival(request):
    """Survival players."""
    return Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
        game_type__exact=1
    ).all()


@api.get(
    path="/players/survival/dead/",
    response=List[PlayerSchema],
    summary="Dead survival players.",
    tags=["players"]
)
def dead(request):
    """Dead survival players."""
    return Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
        game_type__exact=1,
        is_deleted__exact=1
    ).all()


@api.get(
    path="/players/survival/living/",
    response=List[PlayerSchema],
    summary="Living survival players.",
    tags=["players"]
)
def living(request):
    """Living survival players."""
    return Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
        game_type__exact=1,
        is_deleted__exact=0
    ).all()
