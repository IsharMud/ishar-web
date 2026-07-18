from django.urls import path

from .views import (
    SurveyListView,
    SurveyResultsCSVView,
    SurveyResultsView,
    SurveySubmissionView,
    SurveySubmitView,
    SurveyView,
)


urlpatterns = [
    path("", SurveyListView.as_view(), name="surveys"),
    path("<slug:slug>/", SurveyView.as_view(), name="survey"),
    path("<slug:slug>/submit/", SurveySubmitView.as_view(), name="survey_submit"),
    path("<slug:slug>/results/", SurveyResultsView.as_view(), name="survey_results"),
    path(
        "<slug:slug>/results/export/",
        SurveyResultsCSVView.as_view(),
        name="survey_results_csv",
    ),
    path(
        "<slug:slug>/results/<int:pk>/",
        SurveySubmissionView.as_view(),
        name="survey_submission",
    ),
]
