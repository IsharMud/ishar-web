"""
Feedback report detail — full report, timeline, and the staff action panel.
"""
from django.views.generic.detail import DetailView

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from ..models import Feedback


class FeedbackDetailView(EternalRequiredMixin, NeverCacheMixin, DetailView):
    """Single report with its comment timeline and available staff actions."""

    context_object_name = "report"
    http_method_names = ("get",)
    model = Feedback
    template_name = "feedback_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = (
            self.object.comments.all().order_by("id", "created_at")
        )
        # Reports this one has been marked a duplicate of / by.
        context["duplicates"] = self.object.duplicates.all().order_by("-id")
        context["is_god"] = self.request.user.is_god()
        return context
