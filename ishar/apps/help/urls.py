from django.urls import path

from .views import HelpView


urlpatterns = [
    path("", HelpView.as_view(), name="help"),
    path("<help_topic>/", HelpView.as_view(), name="help_page"),
]
