from django.urls import path

from .views.console import SeasonActionView, SeasonConsoleView
from .views.current import CurrentSeasonView
from .views.season import SeasonView
from .views.track import TrackActionView, TrackConsoleView


urlpatterns = [
    path("", CurrentSeasonView.as_view(), name="current_season"),
    path("console/", SeasonConsoleView.as_view(), name="season_console"),
    path(
        "console/run/",
        SeasonActionView.as_view(),
        name="season_console_run",
    ),
    path("console/track/", TrackConsoleView.as_view(), name="track_console"),
    path(
        "console/track/run/",
        TrackActionView.as_view(),
        name="track_console_run",
    ),
    path("<int:season_id>/", SeasonView.as_view(), name="season"),
]
