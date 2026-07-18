"""Connect app URL configuration."""
from django.urls import path

from .views import (
    ConnectView, MapDiscoverView, MapNoteView, MapStateView, MapZonesView,
    ZoneGraphView,
)


urlpatterns = [
    path("", ConnectView.as_view(), name="connect"),
    path("map/graph/<int:vnum>/", ZoneGraphView.as_view(), name="map_graph"),
    path("map/state/<int:zone_id>/", MapStateView.as_view(), name="map_state"),
    path("map/zones/", MapZonesView.as_view(), name="map_zones"),
    path("map/discover/", MapDiscoverView.as_view(), name="map_discover"),
    path("map/note/", MapNoteView.as_view(), name="map_note"),
]
