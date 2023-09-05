from django.conf import settings
from django.views.generic.list import ListView

from ...apps.player.models import Player


class LeadersView(ListView):
    template_name = "leaders.html.djt"
    context_object_name = "leader_players"

    def get_queryset(self):

        return Player.objects.all()
#            true_level__lt=min(settings.IMMORTAL_LEVELS)
#        ).order_by(
#            "-remorts",
#            "-total_renown",
#            "-quests_completed",
#            "-challenges_completed",
#            "deaths"
#        ).all()


class ClassicLeadersView(LeadersView):

    def get_queryset(self):
        return Player.objects.filter(
            true_level__lt=min(settings.IMMORTAL_LEVELS),
            game_type__exact=1
        ).order_by(
            "-remorts",
            "-total_renown",
            "-quests_completed",
            "-challenges_completed",
            "deaths"
        ).all()


class SurvivalLeadersView(LeadersView):

    def get_queryset(self):
        return Player.objects.filter(
            true_level__lt=min(settings.IMMORTAL_LEVELS),
            game_type__exact=1
        ).order_by(
            "-remorts",
            "-total_renown",
            "-quests_completed",
            "-challenges_completed",
            "deaths"
        ).all()
