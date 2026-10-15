from django.urls import path

from apps.fated.views import TensionLeadersView
from apps.leaders.views import LeadersView
from apps.players.models.game_type import GameType


urlpatterns = [
    path("", LeadersView.as_view(), name="leaders"),
    path("all/", LeadersView.as_view(), name="all_leaders"),
    path("tension/", TensionLeadersView.as_view(), name="tension_leaders"),
    path(
        "tension/lifetime/",
        TensionLeadersView.as_view(lifetime=True),
        name="tension_leaders_lifetime",
    ),
]

for num, label in GameType.choices:
    label = label.lower()
    urlpatterns.append(
        path(
            f"{label}/",
            LeadersView.as_view(game_type=num),
            name=f"{label}_leaders"
        )
    )
