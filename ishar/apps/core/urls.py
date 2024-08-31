"""isharmud.com URL configuration."""
from django.urls import include, path

from ishar.apps.help.views import WorldView
from ishar.apps.players.views.who import PlayerWhoView

from .views import HistoryView, HomeView, StartView, SupportView
from .views.auth import IsharLoginView, IsharLogoutView


urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("areas/", WorldView.as_view(), name="areas"),
    path("challenges/", include("ishar.apps.challenges.urls"), name="challenges"),
    path("clients/", include("ishar.apps.clients.urls"), name="clients"),
    path("discord/", include("ishar.apps.discord.urls"), name="discord"),
    path("events/", include("ishar.apps.events.urls"), name="events"),
    path("faq/", include("ishar.apps.faqs.urls"), name="faq"),
    path("help/", include("ishar.apps.help.urls"), name="help"),
    path("history/", HistoryView.as_view(), name="history"),
    path("leaders/", include("ishar.apps.leaders.urls"), name="leaders"),
    path("login/", IsharLoginView.as_view(), name="login"),
    path("logout/", IsharLogoutView.as_view(), name="logout"),
    path("patches/", include("ishar.apps.patches.urls"), name="patches"),
    path("player/", include("ishar.apps.players.urls"), name="player"),
    path("portal/", include("ishar.apps.accounts.urls"), name="portal"),
    path("season/", include("ishar.apps.seasons.urls"), name="season"),
    path("start/", StartView.as_view(), name="start"),
    path("support/", SupportView.as_view(), name="support"),
    path("who/", PlayerWhoView.as_view(), name="who"),
    path("world/", WorldView.as_view(), name="world"),
]
