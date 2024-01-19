from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.base import TemplateView

from ishar.apps.players.models import Player


class PlayerView(LoginRequiredMixin, DetailView):
    """
    Player view.
    """
    context_object_name = "player"
    model = Player
    slug_field = slug_url_kwarg = query_pk_and_slug = "name"
    template_name = "player.html"


class PlayerSearchView(LoginRequiredMixin, TemplateView):
    """
    Player search view.
    """
    template_name = "player.html"
    model = Player
