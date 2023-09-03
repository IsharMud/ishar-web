from django.urls import path, re_path

from .views import HelpView, HelpPageView


urlpatterns = [
    path("", HelpView.as_view(), name="help"),
    re_path(r"^(?P<help_topic>.+)/$", HelpPageView.as_view(), name="help_page")
]
