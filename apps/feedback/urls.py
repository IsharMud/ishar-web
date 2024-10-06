from django.urls import path

from .views.feedback import FeedbackView
from .views.submit import SubmitFeedbackView


urlpatterns = [
    path("", FeedbackView.as_view(), name="feedback"),
    path("submit/", SubmitFeedbackView.as_view(), name="submit_feedback")
]
