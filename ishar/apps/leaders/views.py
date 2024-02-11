from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from ishar.apps.players.models import GameType, Player


class LeadersView(LoginRequiredMixin, ListView):
    """
    Filter and order players to determine leaders.
        Optionally filter for game type, and living/dead.
    """
    model = Player
    context_object_name = "leader_players"
    template_name = "leaders.html"
    deleted = None
    game_type = None
    game_type_name = None

    def get_queryset(self):
        """Filter players."""

        # Exclude immortals.
        qs = self.model.objects.exclude(
            true_level__gte=min(settings.IMMORTAL_LEVELS)[0]
        )

        # Optionally filter for living/dead players.
        if self.deleted is not None:
            qs = qs.filter(is_deleted__exact=self.deleted)

        # Optionally filter game type.
        if self.game_type is not None and self.game_type in GameType:
            self.game_type_name = \
                GameType._value2member_map_[self.game_type].label
            qs = qs.filter(game_type__exact=self.game_type)

        # Order the players based upon their progress,
        #   sorting and returning the "leaders".
        qs = qs.order_by(
            "-remorts", "-total_renown", "-quests_completed",
            "-challenges_completed", "deaths"
        )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        """Include dead/living, game type, and types of games, in context."""
        context = super().get_context_data(object_list=None, **kwargs)
        context["deleted"] = self.deleted
        context["game_type"] = self.game_type
        context["game_type_name"] = self.game_type_name
        context["game_types"] = GameType.choices
        return context
