from django.urls import path

from .views import PatchView


urlpatterns = [
    path("", PatchView.as_view(), name="patches"),
    path("all/", PatchView.as_view(), name="all"),
]
