from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from ishar.apps.players.models import Player

MINIMUM_IMMORTAL = min(settings.IMMORTAL_LEVELS)[0]


class LeadersView(LoginRequiredMixin, ListView):
    """
    Leaders view.
    """
    model = Player
    context_object_name = "leader_players"
    template_name = "leaders.html"
    ordering = (
        "-remorts", "-total_renown", "-quests_completed",
        "-challenges_completed", "deaths"
    )

    game_type = None

    def get_queryset(self):
        qs = self.model.objects.filter(
            true_level__lt=min(settings.IMMORTAL_LEVELS)[0]
        )
        if self.game_type is not None:
            qs = qs.filter(game_type__exact=self.game_type)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["game_type"] = self.game_type
        if context["game_type"] is not None:
            context["game_type"] = settings.GAME_TYPES[self.game_type][1]
        return context


class ClassicLeadersView(LeadersView):
    """
    Classic players leaders view.
    """
    game_type = 0


class SurvivalLeadersView(LeadersView):
    """
    Survival players leaders view.
    """
    game_type = 1
