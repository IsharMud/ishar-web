from .forms import PlayerSearchForm
from .models.player import Player


def player_search_form(request):
    # Context processor for player search form.
    return {"PLAYER_SEARCH_FORM": PlayerSearchForm()}


def players_online(request):
    # Context processor of count of number of players who are online.
    return {"PLAYERS_ONLINE": Player.objects.online().count()}
