from django.urls import path

from .views import GlobalEventsView


urlpatterns = [path("", GlobalEventsView.as_view(), name="events"),]
