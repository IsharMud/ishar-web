from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from ishar.apps.challenges.models import Challenge


class ChallengesView(LoginRequiredMixin, ListView):
    """
    Challenges view.
    """
    context_object_name = "challenges"
    model = Challenge
    queryset = model.objects.filter(is_active__exact=1)
    template_name = "challenges.html"


class CompleteChallengesView(ChallengesView):
    """
    Complete challenges view.
    """
    model = Challenge
    queryset = model.objects.filter(
        is_active__exact=1
    ).exclude(
        winner_desc__exact=""
    )


class IncompleteChallengesView(ChallengesView):
    """
    Complete challenges view.
    """
    model = Challenge
    queryset = model.objects.filter(
        is_active__exact=1,
        winner_desc__exact=""
    )
