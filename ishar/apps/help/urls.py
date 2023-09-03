from django.urls import include, path, re_path

from .views import HelpView, BackgroundView, HistoryView, StartView
from .views.clients import ClientsView
from .views.world import AreasView, WorldView


urlpatterns = [
    path("", HelpView.as_view(), name="help"),
    re_path(r"<help_topic>/", HelpView.as_view(), name="help_page"),
    path("clients/", ClientsView.as_view(), name="clients"),
    path("mudclients/", ClientsView.as_view(), name="mudclients"),
    path("mud_clients/", ClientsView.as_view(), name="mud_clients"),

    path("background/", BackgroundView.as_view(), name="background"),
    path("history/", HistoryView.as_view(), name="history"),

    path("getstarted/", StartView.as_view(), name="getstarted"),
    path("get_started/", StartView.as_view(), name="get_started"),
    path("start/", StartView.as_view(), name="start"),

    path("areas/", AreasView.as_view(), name="areas"),
    path("world/", WorldView.as_view(), name="world"),

]
