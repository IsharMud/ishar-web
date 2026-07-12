from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.expressions import F
from django.utils.timezone import now
from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin

from apps.players.models.player import Player


class PlayerWhoView(LoginRequiredMixin, NeverCacheMixin, ListView):
    """Show online players."""

    context_object_name = "players"
    model = Player
    template_name = "who.html"

    def get_queryset(self):
        # There is no live presence signal yet (isharmud/ishar-mud#1771).
        # "Online" is inferred: logon >= logout alone breaks once the game's
        # 5-minute autosave refreshes logout mid-session, so a recent logout
        # also counts. Just-quit players linger here for up to 10 minutes.
        return super().get_queryset().filter(
            Q(logon__gte=F("logout"))
            | Q(logout__gte=now() - timedelta(minutes=10)),
            is_deleted=False,
        )
