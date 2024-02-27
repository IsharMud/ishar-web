from typing import List

from django.db.models import F

from ishar.apps.core.api import api
from ishar.apps.players.models.player import Player
from ishar.apps.players.api.schemas import BasePlayerSchema


@api.get(
    path="/who/",
    response=List[BasePlayerSchema],
    summary="Players who are currently online..",
    tags=["immortals", "players"]
)
def who(request):
    """Players online."""
    return Player.objects.filter(logon__gte=F("logout")).all()
