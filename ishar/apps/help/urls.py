from django.urls import path

from .views import HelpView, HelpPageView


urlpatterns = [
    path("", HelpView.as_view(), name="help"),
    path("<help_topic>/", HelpPageView.as_view(), name="help_page"),
]
