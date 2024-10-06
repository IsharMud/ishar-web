from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from ..models.choices import FeedbackSubmissionType
from ..models.submission import FeedbackSubmission


class SubmissionView(LoginRequiredMixin, DetailView):
    """Single feedback submission page."""

    context_object_name = "submission"
    http_method_names = ("get",)
    model = FeedbackSubmission
    queryset = model.objects.exclude(private__exact=True).exclude(
        submission_type__exact=FeedbackSubmissionType.COMPLETE
    )
    template_name = "submission.html"
    pk_url_kwarg = "submission_id"
