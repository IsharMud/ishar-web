from .forms import PlayerSearchForm


def player_search_form(request):
    # Context processor for player search form.
    return {"PLAYER_SEARCH_FORM": PlayerSearchForm()}
