from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.core.serializers import serialize
from django.views.generic.list import ListView

from .models.challenge import Challenge


class ChallengesView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    """
    Challenges view.
    """
    completed = None
    context_object_name = "challenges"
    model = Challenge
    permission_required = "challenges.view_challenge"
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context[self.context_object_name] = serialize(
            format="json",
            queryset=context.get(self.context_object_name),
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
            fields=(
                "mobile", "challenge_desc",
                "max_level", "max_people", "winner_desc"
            )
        )
        return context
