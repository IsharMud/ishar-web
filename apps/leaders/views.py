from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin
from apps.players.models.game_type import GameType

from .models import Leader


class LeadersView(LoginRequiredMixin, NeverCacheMixin, ListView):
    """Lead players view."""

    model = Leader
    context_object_name = "leaders"
    template_name = "leaders.html"
    game_type = None

    def setup(self, request, *args, **kwargs):
        if self.game_type is not None:
            if self.game_type not in GameType:
                raise Http404(f"Invalid game type.")
            self.game_type = GameType._value2member_map_[self.game_type]
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        # Pull every related row the table reads — class/level (`common`),
        # renown/challenges/quests/deaths (`statistics`) and privacy
        # (`account`) — in one query, instead of a lookup per player per
        # column. The template reads these relations directly; flattening
        # them onto each instance is avoided because those attribute names
        # (e.g. `quests`) collide with model fields and reverse relations.
        qs = super().get_queryset().select_related(
            "account",
            "common",
            "common__player_class",
            "statistics",
        )
        if self.game_type is not None:
            qs = qs.filter(game_type__exact=self.game_type.value)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):

        # One game mode is live at a time (Classic normally, Hardcore for
        # Fated seasons), so the page shows no game-type filter UI — the
        # per-type URLs stay routable for whenever that changes.
        context = super().get_context_data(object_list=None, **kwargs)
        context["game_type"] = self.game_type
        return context
