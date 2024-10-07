from django.urls import path

from .views.count import VoteCountView
from .views.feedback import FeedbackView
from .views.submit import SubmitFeedbackView
from .views.vote import VoteFeedbackView


urlpatterns = [
    path("", FeedbackView.as_view(), name="feedback"),
    path("vote/<int:submission_id>/", VoteFeedbackView.as_view(), name="vote_feedback"),
    path("vote/<int:submission_id>/count/", VoteCountView.as_view(), name="vote_count"),
    path("submit/", SubmitFeedbackView.as_view(), name="submit_feedback")
]
