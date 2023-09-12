from django.urls import path, re_path

from .views import PlayerView, PlayerSearchView


urlpatterns = [
    path("<slug:name>/", PlayerView.as_view(), name="player"),
    path("", PlayerSearchView.as_view(), name="players"),
]
