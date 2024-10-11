from django.urls import path

from .models.choices import FeedbackSubmissionTypePublic

from .views.feedback import FeedbackView
from .views.submit import SubmitFeedbackView
from .views.vote import VoteFeedbackView


urlpatterns = [
    path("", FeedbackView.as_view(), name="feedback"),
    path("all/", FeedbackView.as_view(), name="all_feedback"),
    path("submit/", SubmitFeedbackView.as_view(), name="submit_feedback"),
    path(
        "vote/<int:submission_id>/",
        VoteFeedbackView.as_view(),
         name="vote_feedback"
    ),
]

for num, label in FeedbackSubmissionTypePublic.choices:
    label = label.lower()
    urlpatterns.append(
        path(
            f"{label}/",
            FeedbackView.as_view(submission_type=num),
            name=f"{label}_feedback"
        )
    )
