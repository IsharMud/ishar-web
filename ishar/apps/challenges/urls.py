from django.urls import path

from .views import ChallengesView


urlpatterns = [
    path("", ChallengesView.as_view(), name="challenges"),
]
