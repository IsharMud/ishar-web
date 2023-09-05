from django.conf import settings
from django.views.generic.list import ListView

from ...apps.player.models import Player


MINIMUM_IMMORTAL = min(settings.IMMORTAL_LEVELS)


class LeadersView(ListView):
    """
    Leaders view.
    """
    context_object_name = "leader_players"
    queryset = Player.objects.filter(
        true_level__lt=MINIMUM_IMMORTAL
    ).order_by(
        "-remorts", "-total_renown", "-quests_completed",
        "-challenges_completed", "deaths"
    )

    template_name = "leaders.html.djt"


class ClassicLeadersView(LeadersView):
    """
    Classic players leaders view.
    """
    queryset = Player.objects.filter(
        true_level__lt=MINIMUM_IMMORTAL,
        game_type__exact=0
    ).order_by(
        "-remorts", "-total_renown", "-quests_completed",
        "-challenges_completed", "deaths"
    )


class SurvivalLeadersView(LeadersView):
    """
    Survival players leaders view.
    """
    queryset = Player.objects.filter(
        true_level__lt=MINIMUM_IMMORTAL,
        game_type__exact=1
    ).order_by(
        "-remorts", "-total_renown", "-quests_completed",
        "-challenges_completed", "deaths"
    )
