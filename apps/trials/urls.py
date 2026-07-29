from django.urls import path

from .views import (
    TrialApplicantActionView,
    TrialApplicationView,
    TrialApplySubmitView,
    TrialApplyView,
    TrialInfoView,
    TrialReviewActionView,
    TrialReviewDashboardView,
    TrialReviewDetailView,
)


urlpatterns = [
    path("", TrialInfoView.as_view(), name="trials"),
    path("apply/", TrialApplyView.as_view(), name="trial_apply"),
    path("apply/submit/", TrialApplySubmitView.as_view(), name="trial_apply_submit"),
    path("application/", TrialApplicationView.as_view(), name="trial_application"),
    path(
        "application/<str:action>/",
        TrialApplicantActionView.as_view(),
        name="trial_applicant_action",
    ),
    path("review/", TrialReviewDashboardView.as_view(), name="trial_review"),
    path(
        "review/<int:pk>/",
        TrialReviewDetailView.as_view(),
        name="trial_review_detail",
    ),
    path(
        "review/<int:pk>/<str:action>/",
        TrialReviewActionView.as_view(),
        name="trial_review_action",
    ),
]
