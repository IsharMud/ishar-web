from django.urls import path

from ishar.apps.challenges.views import (
    ChallengesView, CompleteChallengesView, IncompleteChallengesView
)


urlpatterns = [
    path("", ChallengesView.as_view(), name="challenges"),
    path("complete/", CompleteChallengesView.as_view(), name="complete"),
    path("incomplete/", IncompleteChallengesView.as_view(), name="incomplete"),
]
