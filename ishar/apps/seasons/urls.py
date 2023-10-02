from django.urls import path

from ishar.apps.seasons.util import get_current_season
from ishar.apps.seasons.views import CurrentSeasonView, SeasonView


current_season = get_current_season()

urlpatterns = [
    path("", CurrentSeasonView.as_view(), name="current_season"),
    path("<int:season_id>/", SeasonView.as_view(), name="season"),
]
