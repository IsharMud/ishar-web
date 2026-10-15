from django.urls import path

from .views import AchievementsView


urlpatterns = [
    path("", AchievementsView.as_view(), name="achievements"),
]
