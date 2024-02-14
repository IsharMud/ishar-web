from django.urls import path

from ishar.apps.patches.views import PatchesView, PatchesLatestView


urlpatterns = [
    path("", PatchesView.as_view(), name="patches"),
    path("all/", PatchesView.as_view(), name="all"),
    path("latest/", PatchesLatestView.as_view(), name="latest"),
]
