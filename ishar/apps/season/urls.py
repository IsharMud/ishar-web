from django.urls import path

from .views import SeasonView


urlpatterns = [
    path("", SeasonView.as_view(), name="season"),
]
