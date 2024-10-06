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
    paginate_by = 3
    queryset = model.objects.exclude(
        submission_type__exact=FeedbackSubmissionType.COMPLETE
    )
    template_name = "feedback.html"
    feedback_admin = False

    def setup(self, request, *args, **kwargs):
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                self.feedback_admin = True
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.feedback_admin is True:
            return qs
        return qs.exclude(private__exact=True)
