from django.urls import path

from .views import PatchListView, PatchAllView


urlpatterns = [
    path("", PatchListView.as_view(), name="patches"),
    path("all/", PatchAllView.as_view(), name="all"),
]
