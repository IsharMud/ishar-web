from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin

from ..models.choices import FeedbackSubmissionType
from ..models.submission import FeedbackSubmission


class AllFeedbackView(LoginRequiredMixin, NeverCacheMixin, ListView):
    """All feedback list page."""

    context_object_name = "submissions"
    http_method_names = ("get",)
    model = FeedbackSubmission
    queryset = model.objects.exclude(private__exact=True).exclude(
        submission_type__exact=FeedbackSubmissionType.COMPLETE
    )
    template_name = "all.html"
