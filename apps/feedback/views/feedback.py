from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin

from ..models.choices import FeedbackSubmissionType
from ..models.submission import FeedbackSubmission


class FeedbackView(LoginRequiredMixin, NeverCacheMixin, ListView):
    """All feedback list page."""

    context_object_name = "submissions"
    http_method_names = ("get",)
    model = FeedbackSubmission
    paginate_by = 5
    queryset = model.objects.exclude(
        submission_type__exact=FeedbackSubmissionType.COMPLETE
    )
    template_name = "feedback.html"
