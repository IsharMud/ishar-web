from django.http.response import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin

from ..models.choices import FeedbackSubmissionType, FeedbackSubmissionTypePublic
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
    submission_type = None
    template_name = "feedback.html"


    def setup(self, request, *args, **kwargs):
        if self.submission_type is not None:
            if self.submission_type not in FeedbackSubmissionTypePublic:
                raise Http404(f"Invalid submission type.")
            self.submission_type = \
                FeedbackSubmissionType._value2member_map_[self.submission_type]
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.submission_type is not None:
            qs = qs.filter(submission_type__exact=self.submission_type)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["submission_type"] = self.submission_type
        context["submission_types"] = FeedbackSubmissionTypePublic.choices
        return context
