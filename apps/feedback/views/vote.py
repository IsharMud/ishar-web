from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin

from ..models.submission import FeedbackSubmission
from ..models.vote import FeedbackVote


class VoteFeedbackView(LoginRequiredMixin, NeverCacheMixin, View):
    """Votes on feedback submissions."""

    http_method_names = ("get", "post")
    submission = None
    vote = None
    vote_obj = None

    def setup(self, request, *args, **kwargs):
        submission_id = kwargs.get("submission_id")
        try:
            self.submission = FeedbackSubmission.objects.get(pk=submission_id)
        except FeedbackSubmission.DoesNotExist as nsub:
            raise Http404(f"No such feedback: {submission_id}.") from nsub
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.vote_obj = FeedbackVote.objects.get(
                feedback_submission=self.submission,
                account=request.user
            )
            self.vote = self.vote_obj.vote_value
        except FeedbackVote.DoesNotExist:
            self.vote = None

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._json_response()

    def post(self, request, *args, **kwargs):
        if isinstance(self.vote_obj, FeedbackVote):
            self.vote_obj.delete()
            self.vote = None

        else:
            self.vote_obj, created = FeedbackVote.objects.update_or_create(
                feedback_submission=self.submission,
                account=request.user,
                defaults={"vote_value": True},
            )
            self.vote = self.vote_obj.vote_value

        return self._json_response()

    def _json_response(self):
        return JsonResponse(
            data={
                "vote": self.vote,
                "total": self.submission.vote_total
            }
        )