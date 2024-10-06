from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin

from ..models.submission import FeedbackSubmission
from ..models.vote import FeedbackVote


class VoteFeedbackView(NeverCacheMixin, LoginRequiredMixin, View):
    """
    Vote on feedback submissions, via JavaScript AJAX/XMLHttpRequest ("XHR").
    """
    http_method_names = ("get",)
    status = 200
    submission = None
    vote = None

    def setup(self, request, *args, **kwargs):
        submission_id = kwargs.get("submission_id")
        try:
            self.submission = FeedbackSubmission.objects.get(pk=submission_id)
        except FeedbackSubmission.DoesNotExist as no_sub:
            raise Http404(f"No such feedback: {submission_id}.") from no_sub
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.submission is not None:
            try:
                self.vote = FeedbackVote.objects.get(
                    feedback_submission=self.submission,
                    account=request.user
                ).vote_value
                self.status = 202
            except FeedbackVote.DoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse(data={"vote": self.vote}, status=self.status)
