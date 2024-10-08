from django.urls import path

from .views import HistoryView


urlpatterns = [
    path("", HistoryView.as_view(), name="history"),
]
