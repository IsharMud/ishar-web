from django.urls import path

from ishar.apps.events.views import GlobalEventsView


urlpatterns = [
    path("", GlobalEventsView.as_view(), name="events"),
]
