from django.views.generic.base import TemplateView

from apps.connect.skill_icons import SKILL_ICONS


class ConnectView(TemplateView):
    """MUD web client connection page."""

    template_name = "connect.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # The standardized skill→icon map the HUD inherits (id → game-icons
        # name). Rendered via {{ ...|json_script }} so it reaches the page as
        # safely-escaped JSON, then handed to IsharHUD.init({skillIcons}).
        ctx["skill_icons"] = SKILL_ICONS
        return ctx
