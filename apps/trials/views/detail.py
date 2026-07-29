"""
Trial application detail — the full application, complete timeline (internal
notes included), live eligibility, and the staff action panel.
"""
from django.views.generic.detail import DetailView

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from .. import eligibility
from ..models import TrialApplication


class TrialReviewDetailView(EternalRequiredMixin, NeverCacheMixin, DetailView):
    """Single application with its timeline and available staff actions."""

    context_object_name = "application"
    http_method_names = ("get",)
    model = TrialApplication
    template_name = "trial_review_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("account")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timeline"] = self.object.comments.all()
        context["eligibility"] = eligibility.check(self.object.account)
        # A re-applicant's history is context reviewers need.
        context["prior_applications"] = (
            TrialApplication.objects.filter(account=self.object.account)
            .exclude(pk=self.object.pk)
            .order_by("-id")
        )
        return context
