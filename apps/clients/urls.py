from django.urls import path

from apps.clients.views import MUDClientsView


urlpatterns = [path("", MUDClientsView.as_view(), name="clients"),]
