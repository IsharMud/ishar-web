"""isharmud.com ASGI configuration."""
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from apps.connect.routing import websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # The origin validator matters since connect auto-login (#85): the
    # websocket now carries the portal session's authority into the game, so
    # a cross-site page must not be able to open it with a rider's cookies.
    # SESSION_COOKIE_SAMESITE=Strict already blocks that in modern browsers;
    # this is the canonical second layer.
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
