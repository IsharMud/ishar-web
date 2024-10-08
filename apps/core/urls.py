from django.urls import path

from apps.help.views import WorldView
from apps.players.views.who import PlayerWhoView

from .views import HomeView, StartView, UpgradesView, SupportView
from .views.auth import IsharLoginView, IsharLogoutView


urlpatterns = [
    path("", HomeView.as_view(), name="index"),

    # Authentication.
    path("login/", IsharLoginView.as_view(), name="login"),
    path("logout/", IsharLogoutView.as_view(), name="logout"),

    path("start/", StartView.as_view(), name="start"),
    path("support/", SupportView.as_view(), name="support"),
    path("upgrades/", UpgradesView.as_view(), name="upgrades"),
    path("who/", PlayerWhoView.as_view(), name="who"),
    path("areas/", WorldView.as_view(), name="areas"),
    path("world/", WorldView.as_view(), name="world"),

]
