from django.urls import path

from .views import ChallengesView


urlpatterns = [
    path("", ChallengesView.as_view(), name="challenges"),
    path(
        "complete/",
        ChallengesView.as_view(completed=True),
        name="complete"
    ),
    path(
        "incomplete/",
        ChallengesView.as_view(completed=False),
        name="incomplete"
    ),
]
