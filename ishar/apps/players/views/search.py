from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from ishar.apps.players.models.player import Player


class PlayerSearchView(LoginRequiredMixin, TemplateView):
    """
    Player search view.
    """
    template_name = "player.html"
    model = Player
