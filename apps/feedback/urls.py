from django.urls import path

from .views.all import AllFeedbackView
from .views.feedback import FeedbackView
from .views.submission import SubmissionView
from .views.submit import SubmitFeedbackView


urlpatterns = [

    path(
        "",
        FeedbackView.as_view(),
        name="feedback"
    ),

    path(
        "submit/",
        SubmitFeedbackView.as_view(),
        name="submit_feedback"
    ),

    path(
        "all/",
        AllFeedbackView.as_view(),
        name="all_feedback"
    ),

    path(
        "<int:submission_id>/",
        SubmissionView.as_view(),
        name="feedback_submission"
    )
]
