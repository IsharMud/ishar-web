"""Connect app URL configuration."""
from django.urls import path

from .views import (
    ConnectView, HudBarView, MapDiscoverView, MapNoteView, MapStateView,
    MapZonesView, QuestCatalogView, QuestTrackedView, QuestTrackView,
    ZoneGraphView,
)


urlpatterns = [
    path("", ConnectView.as_view(), name="connect"),
    path("map/graph/<int:vnum>/", ZoneGraphView.as_view(), name="map_graph"),
    path("map/state/<int:zone_id>/", MapStateView.as_view(), name="map_state"),
    path("map/zones/", MapZonesView.as_view(), name="map_zones"),
    path("map/discover/", MapDiscoverView.as_view(), name="map_discover"),
    path("map/note/", MapNoteView.as_view(), name="map_note"),
    path("quests/catalog/", QuestCatalogView.as_view(), name="quest_catalog"),
    path("quests/tracked/", QuestTrackedView.as_view(), name="quest_tracked"),
    path("quests/track/", QuestTrackView.as_view(), name="quest_track"),
    path("hud/bar/", HudBarView.as_view(), name="hud_bar"),
]
