from django.urls import path

from .views import PatchesAllView, PatchesLatestView, PatchesListView


urlpatterns = [
    path("", PatchesListView.as_view(), name="patches"),
    path("all/", PatchesAllView.as_view(), name="all"),
    path("latest/", PatchesLatestView.as_view(), name="latest"),
]
