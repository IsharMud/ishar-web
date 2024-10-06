from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class FeedbackView(LoginRequiredMixin, TemplateView):
    """Feedback main page."""

    http_method_names = ("get",)
    template_name = "feedback.html"
