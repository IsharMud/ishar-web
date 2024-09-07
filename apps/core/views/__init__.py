from django.views.generic.base import TemplateView

from .error import ErrorView
from .home import HomeView
from .upgrades import UpgradesView


class HistoryView(TemplateView):
    """History page."""
    template_name = "history.html"

class StartView(TemplateView):
    """Getting started guide."""
    template_name = "start.html"

class SupportView(TemplateView):
    """Information about how to support Ishar MUD."""
    template_name = "support.html"
