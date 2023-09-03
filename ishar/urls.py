from django.urls import include, path

from .api import api_router
from .views import (
    ConnectRedirectView, HistoryView, StartView, SupportView, WelcomeView
)
from .views.clients import ClientsView
# from .views.events import EventsView

from .views.faq import FAQView

from .apps.help.views import WorldView


urlpatterns = [
    path("", WelcomeView.as_view(), name="index"),

    # path("account/", include("ishar.apps.account.urls"), name="account"),
    path("api/", include(api_router.urls), name="api"),

    path("clients/", ClientsView.as_view(), name="clients"),
    path("mudclients/", ClientsView.as_view(), name="mudclients"),
    path("mud_clients/", ClientsView.as_view(), name="mud_clients"),

    path("background/", HistoryView.as_view(), name="background"),
    path("history/", HistoryView.as_view(), name="history"),

    path("connect/", ConnectRedirectView.as_view(), name="connect"),

    path("faq/", FAQView.as_view(), name="faq"),
    path("faqs/", FAQView.as_view(), name="faqs"),
    path("questions/", FAQView.as_view(), name="questions"),

    path("getstarted/", StartView.as_view(), name="getstarted"),
    path("get_started/", StartView.as_view(), name="get_started"),
    path("start/", StartView.as_view(), name="start"),

    # path("events/", EventsView.as_view(), name="events"),

    path("help/", include("ishar.apps.help.urls"), name="help"),
    path("patches/", include("ishar.apps.patches.urls"), name="patches"),
    path("portal", WelcomeView.as_view(), name="portal"),
    path("season/", include("ishar.apps.season.urls"), name="season"),
    path("support/", SupportView.as_view(), name="support"),

    path("areas/", WorldView.as_view(), name="areas"),
    path("world/", WorldView.as_view(), name="world"),
]
