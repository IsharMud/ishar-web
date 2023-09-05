from django.conf import settings
from django.views.generic.list import ListView

from ...apps.player.models import Player


class LeadersView(ListView):
    """
    Leaders view.
    """
    model = Player
    template_name = "leaders.html.djt"
    context_object_name = "leader_players"

    queryset = model.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)
    ).order_by(
        "-remorts", "-total_renown", "-quests_completed",
        "-challenges_completed", "deaths"
    )


class ClassicLeadersView(LeadersView):
    """
    Classic players leaders view.
    """
    model = Player
    queryset = model.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS), game_type__exact=0
    ).order_by(
        "-remorts", "-total_renown", "-quests_completed",
        "-challenges_completed", "deaths"
    )


class SurvivalLeadersView(LeadersView):
    """
    Survival players leaders view.
    """
    model = Player
    queryset = model.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS), game_type__exact=1
    ).order_by(
        "-remorts", "-total_renown", "-quests_completed",
        "-challenges_completed", "deaths"
    )
