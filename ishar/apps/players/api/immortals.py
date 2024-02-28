from typing import List

from django.conf import settings

from ishar.apps.core.api import api
from ishar.apps.players.models.player import Player
from ishar.apps.players.api.schemas import ImmortalSchema


@api.get(
    path="/immortals/",
    response=List[ImmortalSchema],
    summary="Immortals.",
    tags=["immortals", "players"]
)
def immortals(request):
    """Immortals."""
    return Player.objects.filter(
        true_level__gte=settings.MIN_IMMORTAL_LEVEL
    ).all()
