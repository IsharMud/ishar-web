from django.urls import path

from apps.leaders.views import LeadersView
from apps.players.models.game_type import GameType


urlpatterns = [
    path("", LeadersView.as_view(), name="leaders"),
    path("all/", LeadersView.as_view(), name="all_leaders"),
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
