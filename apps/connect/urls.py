"""Connect app URL configuration."""
from django.urls import path

from .views import ConnectView


urlpatterns = [
    path("", ConnectView.as_view(), name="connect"),
]
