from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from ishar.apps.players.models import Player


class LeadersView(LoginRequiredMixin, ListView):
    """
    Filter and order players to determine leaders.
        Optional filter for game type:
            Classic = 0, Survival = 1, All = None
            (used by child classes)
    """
    model = Player
    context_object_name = "leader_players"
    template_name = "leaders.html"
    game_type = None

    def get_queryset(self):
        """Filter players."""

        # Exclude immortals players.
        qs = self.model.objects.filter(
            true_level__lt=min(settings.IMMORTAL_LEVELS)[0]
        )

        # Optionally filter game type (Classic/Survival).
        if self.game_type is not None:
            qs = qs.filter(game_type__exact=self.game_type)

        # Order the players based upon their progress,
        #   sorting and returning the "leaders".
        qs = qs.order_by(
            "-remorts", "-total_renown", "-quests_completed",
            "-challenges_completed", "deaths"
        )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        """Include friendly name of any optional game type in context."""
        context = super().get_context_data(object_list=None, **kwargs)
        context["game_type"] = self.game_type
        if context["game_type"] is not None:
            context["game_type"] = settings.GAME_TYPES[self.game_type][1]
        return context


class ClassicLeadersView(LeadersView):
    """Classic players leaders view."""
    game_type = 0


class SurvivalLeadersView(LeadersView):
    """Survival players leaders view."""
    game_type = 1
    deleted = None

    def get_context_data(self, *, object_list=None, **kwargs):
        """Include boolean when viewing dead or living survival players."""
        context = super().get_context_data(object_list=None, **kwargs)
        context["deleted"] = self.deleted
        return context

    def get_queryset(self):
        """Filter survival players."""
        qs = super().get_queryset()

        # Optionally filter is_deleted (Dead/Living).
        if self.deleted is not None:
            qs = qs.filter(is_deleted__exact=self.deleted)

        return qs


class SurvivalDeadLeadersView(SurvivalLeadersView):
    """Dead survival players leaders view."""
    deleted = 1


class SurvivalLivingLeadersView(SurvivalLeadersView):
    """Living survival players leaders view."""
    deleted = 0
