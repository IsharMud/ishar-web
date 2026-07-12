from django.urls import path

from .views import EventActionView, EventsConsoleView, GlobalEventsView


urlpatterns = [
    path("", GlobalEventsView.as_view(), name="events"),
    path("console/", EventsConsoleView.as_view(), name="events_console"),
    path("console/run/", EventActionView.as_view(), name="events_console_run"),
]
