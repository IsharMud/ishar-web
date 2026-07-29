"""
Public Immortal Trial page — the policy summary that recruits, plus a
state-aware call to action for logged-in players.
"""
from django.views.generic.base import TemplateView

from .. import eligibility
from ..models import TrialApplication


class TrialInfoView(TemplateView):
    """What the trial is, what it expects, and how to apply."""

    template_name = "trials.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context["eligibility"] = eligibility.check(user)
            context["application"] = (
                TrialApplication.objects.filter(account=user)
                .order_by("-id")
                .first()
            )
        return context
