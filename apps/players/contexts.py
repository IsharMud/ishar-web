from django.db.models import F
from .forms import PlayerSearchForm
from .models.player import Player


def player_search_form(request):
    # Context processor for player search form.
    return {"PLAYER_SEARCH_FORM": PlayerSearchForm()}


def players_online(request):
    # Context processor of count of number of players who are online.
    return {
        "PLAYERS_ONLINE": Player.objects.filter(
                logon__gte=F("logout"),
                is_deleted=False,
                online__gt=0
            ).count()
    }
