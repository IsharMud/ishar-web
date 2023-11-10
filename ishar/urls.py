"""
isharmud.com URL configuration.
"""
from django.urls import include, path

from ishar.api import api_router
from ishar.views import SupportView, WelcomeView
from ishar.views.auth import IsharLoginView, IsharLogoutView
from ishar.apps.help.views import WorldView


urlpatterns = [
    path("", WelcomeView.as_view(), name="index"),
    path("api/", include(api_router.urls), name="api"),
    path("areas/", WorldView.as_view(), name="areas"),
    path("challenges/", include("ishar.apps.challenges.urls"), name="challenges"),
    path("clients/", include("ishar.apps.clients.urls"), name="clients"),
    path("events/", include("ishar.apps.events.urls"), name="events"),
    path("faq/", include("ishar.apps.faqs.urls"), name="faq"),
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
