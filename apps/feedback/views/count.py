from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin

from ..models.choices import FeedbackSubmissionTypePublic
from ..models.submission import FeedbackSubmission


class VoteCountView(NeverCacheMixin, LoginRequiredMixin, View):
    """Votes on feedback submissions."""
    http_method_names = ("get",)
    status = 400
    submission = None
    vote = None

    def setup(self, request, *args, **kwargs):
        submission_id = kwargs.get("submission_id")
        if request.user and request.user.is_authenticated:
            try:
                self.submission = FeedbackSubmission.objects.get(
                    pk=submission_id,
                    submission_type__in=FeedbackSubmissionTypePublic,
                    private=False
                )
            except FeedbackSubmission.DoesNotExist as no_sub:
                raise Http404(f"No such feedback: {submission_id}.") from no_sub
        else:
            self.status = 401
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.submission is not None:
            self.status = 200
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = {
            "status": self.status,
            "vote_total": self.submission.vote_total
        }
        return JsonResponse(data=data, status=self.status)
