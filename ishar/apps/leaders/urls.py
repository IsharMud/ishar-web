from django.urls import path
from django.views.generic import RedirectView

from ishar.apps.leaders.views import (
    LeadersView, ClassicLeadersView, SurvivalLeadersView,
    SurvivalDeadLeadersView, SurvivalLivingLeadersView
)


urlpatterns = [
    path("", LeadersView.as_view(), name="leaders"),
    path("all/", RedirectView.as_view(url="/leaders"), name="all"),
    path("classic/", ClassicLeadersView.as_view(), name="classic"),
    path("survival/", SurvivalLeadersView.as_view(), name="survival"),
    path(
        "survival/dead/", SurvivalDeadLeadersView.as_view(),
        name="dead_survival"
    ),
    path(
        "survival/living/", SurvivalLivingLeadersView.as_view(),
        name="living_survival"
    )
]
