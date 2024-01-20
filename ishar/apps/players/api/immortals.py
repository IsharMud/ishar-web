from typing import List

from django.conf import settings

from ishar.api import api
from ishar.apps.players.models import Player
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
        true_level__gte=min(settings.IMMORTAL_LEVELS)[0]
    ).all()
