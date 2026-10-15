from django.urls import path

from .views import FatedView, KnotsView


urlpatterns = [
    path("", FatedView.as_view(), name="fated"),
    path("knots/", KnotsView.as_view(), name="knots"),
]
