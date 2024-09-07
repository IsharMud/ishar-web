from django.urls import path

from apps.players.views.player import PlayerView
from apps.players.views.search import PlayerSearchView


urlpatterns = [
    path("<slug:name>/", PlayerView.as_view(), name="player"),
    path("", PlayerSearchView.as_view(), name="players"),
]
