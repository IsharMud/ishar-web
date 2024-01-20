from typing import List

from ishar.api import api
from ishar.apps.players.models import Player
from ishar.apps.players.api.schemas import PlayerSchema


@api.get(
    path="/players/classic/",
    response=List[PlayerSchema],
    summary="Classic players.",
    tags=["players"]
)
def classic(request):
    """Classic players."""
    return Player.objects.filter(game_type__exact=0).all()
