from django.urls import path

from .views.current import CurrentSeasonView
from .views.season import SeasonView


urlpatterns = [
    path("", CurrentSeasonView.as_view(), name="current_season"),
    path("<int:season_id>/", SeasonView.as_view(), name="season"),
]
