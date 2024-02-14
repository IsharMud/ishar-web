from typing import List

from ishar.api import api
from ishar.apps.players.models.game_type import GameType
from ishar.apps.players.models.player import Player
from ishar.apps.players.api.schemas import PlayerSchema


@api.get(
    path="/players/classic/",
    response=List[PlayerSchema],
    summary="Classic players.",
    tags=["players"]
)
def classic(request):
    """Classic players."""
    return Player.objects.filter(game_type__exact=GameType.CLASSIC).all()
