from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from ishar.apps.challenges.models import Challenge


class ChallengesView(LoginRequiredMixin, ListView):
    """
    Challenges view.
    """
    completed = None
    context_object_name = "challenges"
    model = Challenge
    template_name = "challenges.html"

    def get_queryset(self):
        # Filter queryset.
        qs = super().get_queryset()

        # Find active challenges.
        qs = qs.filter(is_active__exact=1)

        # Optional filter by completion.
        if self.completed is not None:
            if self.completed is False:
                qs = qs.filter(winner_desc__exact="")
            if self.completed is True:
                qs = qs.exclude(winner_desc__exact="")

        return qs
