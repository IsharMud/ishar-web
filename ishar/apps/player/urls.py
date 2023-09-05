from django.urls import path, re_path

from .views import PlayerView, PlayerPageView


urlpatterns = [
    path("", PlayerView.as_view(), name="players"),
    re_path(r"^(?P<player_name>.+)/$", PlayerPageView.as_view(), name="player")
]
