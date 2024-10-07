from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin

from ..models.choices import FeedbackSubmissionTypePublic
from ..models.submission import FeedbackSubmission
from ..models.vote import FeedbackVote


class VoteFeedbackView(NeverCacheMixin, LoginRequiredMixin, View):
    """
    Vote on feedback submissions, via JavaScript AJAX/XMLHttpRequest ("XHR").
    """
    http_method_names = ("get", "post",)
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
            try:
                self.vote = FeedbackVote.objects.get(
                    feedback_submission=self.submission,
                    account=request.user
                )
                self.status = 200
            except FeedbackVote.DoesNotExist:
                self.status = 204
                pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.final_response()

    def post(self, request, *args, **kwargs):
        if self.submission:
            if self.vote is not None:
                if self.vote.vote_value is True:
                    self.vote.delete()
                    self.vote = None
                    self.status = 202
                    return self.final_response()

            self.vote, created = FeedbackVote.objects.update_or_create(
                vote_value=True,
                defaults={
                    "account": request.user,
                    "feedback_submission": self.submission
                }
            )
            self.vote.save()
            self.status = 201
        return self.final_response()

    def final_response(self, **kwargs):
        data = {
            "status": self.status,
            "vote": {},
            **kwargs
        }
        if self.vote is not None:
            data["vote"] = {
                "value": self.vote.vote_value,
                "voted": self.vote.voted
            }
        return JsonResponse(data=data, status=self.status)
