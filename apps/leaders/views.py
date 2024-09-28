from django.http import Http404
from django.views.generic.list import ListView

from apps.players.models.game_type import GameType
from .models.leader import Leader


class LeadersView(ListView):

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
        qs = super().get_queryset()
        if self.game_type is not None:
            qs = qs.filter(game_type__exact=self.game_type.value)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(object_list=None, **kwargs)
        context["game_type"] = self.game_type
        context["game_types"] = GameType.choices

        for i in context[self.context_object_name]:
            i.challenges = i.statistics.total_challenges
            i.quests = i.statistics.total_quests
            i.deaths = i.statistics.total_deaths
            i.level = i.common.level
            i.renown = i.statistics.total_renown

        return context
