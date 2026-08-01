from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView

from apps.connect import testserver
from apps.connect.skill_icons import SKILL_ICONS


@method_decorator(ensure_csrf_cookie, name="get")
class ConnectView(TemplateView):
    """MUD web client connection page.

    ``ensure_csrf_cookie`` guarantees the CSRF cookie is set so the HUD
    map's POST endpoints (``hud-map.js``) can send ``X-CSRFToken``.
    """

    template_name = "connect.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # The standardized skill→icon map the HUD inherits (id → game-icons
        # name). Rendered via {{ ...|json_script }} so it reaches the page as
        # safely-escaped JSON, then handed to IsharHUD.init({skillIcons}).
        ctx["skill_icons"] = SKILL_ICONS
        # Advisory only — the websocket consumer re-checks before dialing.
        # The tier shapes client-side copy (announcement, refusal hints).
        ctx["test_server_allowed"] = testserver.allowed(self.request.user)
        ctx["test_server_tier"] = testserver.tier()
        return ctx
