from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView

from .views import InteractionsView


urlpatterns = [
    # Redirect to Discord invitation.
    path("", RedirectView.as_view(url=settings.DISCORD["URL"]), name="discord"),
    # Discord interactions view.
    path("interactions/", InteractionsView.as_view(), name="interactions"),
]
