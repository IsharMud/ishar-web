from django.urls import path

from .views import PatchView, LatestPatchView, TextPatchView


urlpatterns = [
    path("", PatchView.as_view(), name="patches"),
    path("all/", PatchView.as_view(), name="all"),
    path("latest/", LatestPatchView.as_view(), name="latest"),
    path("text/", TextPatchView.as_view(), name="text")
]
