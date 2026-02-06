"""WebSocket URL routing for the connect app."""
from django.urls import path

from .consumers import TelnetConsumer


websocket_urlpatterns = [
    path("ws/connect", TelnetConsumer.as_asgi()),
]
