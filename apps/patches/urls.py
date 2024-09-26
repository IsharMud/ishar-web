from django.urls import path

from apps.patches.views import PatchesView, PatchesLatestView


urlpatterns = [
    path("", PatchesView.as_view(), name="patches"),
    path("latest/", PatchesLatestView.as_view(), name="latestpatch"),
]
