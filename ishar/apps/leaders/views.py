from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.views.generic.list import ListView

from ishar.apps.players.models.game_type import GameType
from .models.leader import Leader


class LeadersView(LoginRequiredMixin, ListView):
    """Filter and order players to determine leaders.
        Optionally filter for game type, and living/dead."""
    model = Leader
    context_object_name = "leaders"
    template_name = "leaders.html"
    deleted = None
    game_type = None
    game_type_name = None

    def get_queryset(self):
        """Filter Leader proxy model."""
        qs = super().get_queryset()

        # Optionally filter for living/dead players.
        if self.deleted is not None:
            qs = qs.filter(is_deleted__exact=self.deleted)

        # Optionally filter game type.
        if self.game_type is not None and self.game_type in GameType:
            self.game_type_name = \
                GameType._value2member_map_[self.game_type].label
            qs = qs.filter(game_type__exact=self.game_type)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        """Include dead/living, game type, and types of games, in context,
            and overwrite appropriate values using player_stats."""
        context = super().get_context_data(object_list=None, **kwargs)
        context["deleted"] = self.deleted
        context["game_type"] = self.game_type
        context["game_type_name"] = self.game_type_name
        context["game_types"] = GameType.choices

        for i in context[self.context_object_name]:
            i.challenges_completed = i.statistics.total_challenges
            i.deaths = i.statistics.total_deaths
            i.true_level = i.common.level
            i.total_renown = i.statistics.total_renown

        context[self.context_object_name] = serialize(
            format="json",
            queryset=context.get(self.context_object_name),
            fields=(
                "name", "remorts", "total_renown", "challenges_completed",
                "deaths", "true_level"
            )
        )
        return context
