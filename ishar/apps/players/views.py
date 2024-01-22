from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

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


class PlayerWhoView(LoginRequiredMixin, ListView):
    """
    "Who" view shows online players.
    """
    context_object_name = "players"
    model = Player
    template_name = "who.html"

    def get_queryset(self):
        return super().get_queryset().filter(logon__gte=F("logout"))
