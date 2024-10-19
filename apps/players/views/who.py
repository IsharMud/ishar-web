from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin

from apps.players.models.player import Player


class PlayerWhoView(LoginRequiredMixin, NeverCacheMixin, ListView):
    """Show online players."""

    context_object_name = "players"
    model = Player
    template_name = "who.html"

    def get_queryset(self):
        return super().get_queryset().filter(logon__gte=F("logout"))
