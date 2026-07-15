"""isharmud.com ASGI configuration."""
import os
import django
from django.core.asgi import get_asgi_application

# 1. Set environment variables first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# 2. Initialize Django before importing any application routing/models
django.setup()

# 3. Now it is safe to import channels and your local routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from apps.connect.routing import websocket_urlpatterns

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
