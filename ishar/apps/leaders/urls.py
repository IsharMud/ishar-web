from django.urls import path

from .views import LeadersView, ClassicLeadersView, SurvivalLeadersView


urlpatterns = [
    path("", LeadersView.as_view(), name="leaders"),
    path("classic/", ClassicLeadersView.as_view(), name="classic"),
    path("survival/", SurvivalLeadersView.as_view(), name="survival"),
]
