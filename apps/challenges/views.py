from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin

from .models.challenge import Challenge


class ChallengesView(NeverCacheMixin, ListView):
    """Challenges view."""
    completed = None
    context_object_name = "challenges"
    model = Challenge
    template_name = "challenges.html"

    def get_queryset(self):
        # Find only active challenges.
        qs = super().get_queryset()
        qs = qs.filter(is_active__exact=1)

        # Optionally filter challenges by completion.
        if self.completed is not None:
            if self.completed is False:
                qs = qs.filter(winner_desc__exact="")
            if self.completed is True:
                qs = qs.exclude(winner_desc__exact="")

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["completed"] = self.completed
        return context
