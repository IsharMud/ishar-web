from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from apps.core.views.mixins import NeverCacheMixin


class FeedbackView(LoginRequiredMixin, NeverCacheMixin, TemplateView):
    """Feedback main page."""

    http_method_names = ("get",)
    template_name = "feedback.html"
