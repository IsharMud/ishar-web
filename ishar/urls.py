"""
isharmud.com URL configuration.
"""
from django.urls import include, path

from ishar.api import api_router
from ishar.faq import FAQView
from ishar.views import (
    ClientsView, HistoryView, IsharLoginView, IsharLogoutView,
    StartView, SupportView, WelcomeView
)

from ishar.apps.help.views import WorldView


urlpatterns = [
    path("", WelcomeView.as_view(), name="index"),

    path("api/", include(api_router.urls), name="api"),

    path("areas/", WorldView.as_view(), name="areas"),

    path("challenges/", include("ishar.apps.challenges.urls"), name="challenges"),

    path("clients/", ClientsView.as_view(), name="clients"),
    path("mudclients/", ClientsView.as_view(), name="mudclients"),
    path("mud_clients/", ClientsView.as_view(), name="mud_clients"),

    path("events/", include("ishar.apps.events.urls"), name="events"),

    path("background/", HistoryView.as_view(), name="background"),
    path("history/", HistoryView.as_view(), name="history"),

    path("faq/", FAQView.as_view(), name="faq"),
    path("faqs/", FAQView.as_view(), name="faqs"),
    path("questions/", FAQView.as_view(), name="questions"),

    path("getstarted/", StartView.as_view(), name="getstarted"),
    path("get_started/", StartView.as_view(), name="get_started"),
    path("start/", StartView.as_view(), name="start"),

    path("help/", include("ishar.apps.help.urls"), name="help"),
    path("leaders/", include("ishar.apps.leaders.urls"), name="leaders"),

    path("login/", IsharLoginView.as_view(), name="login"),
    path("logout/", IsharLogoutView.as_view(), name="logout"),

    path("patches/", include("ishar.apps.patches.urls"), name="patches"),
    path("player/", include("ishar.apps.players.urls"), name="player"),
    path("portal/", include("ishar.apps.accounts.urls"), name="portal"),
    path("season/", include("ishar.apps.seasons.urls"), name="season"),

    path("support/", SupportView.as_view(), name="support"),
    path("world/", WorldView.as_view(), name="world"),
]
