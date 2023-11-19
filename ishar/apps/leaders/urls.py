from django.urls import path
from django.views.generic import RedirectView

from ishar.apps.leaders.views import (
    LeadersView, ClassicLeadersView, SurvivalLeadersView
)


urlpatterns = [
    path("", LeadersView.as_view(), name="leaders"),
    path("all/", RedirectView.as_view(url="/leaders"), name="all"),
    path("classic/", ClassicLeadersView.as_view(), name="classic"),
    path("survival/", SurvivalLeadersView.as_view(), name="survival"),
]
