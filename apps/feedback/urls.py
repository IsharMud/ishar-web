from django.urls import path

from .views import (
    FeedbackActionView,
    FeedbackDashboardView,
    FeedbackDetailView,
)


urlpatterns = [
    path("", FeedbackDashboardView.as_view(), name="feedback"),
    path("<int:pk>/", FeedbackDetailView.as_view(), name="feedback_detail"),
    path(
        "<int:pk>/<str:action>/",
        FeedbackActionView.as_view(),
        name="feedback_action",
    ),
]
