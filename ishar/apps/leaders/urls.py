from django.urls import path
from django.views.generic import RedirectView

from ishar.apps.leaders.views import LeadersView
from ishar.apps.players.models.game_type import GameType


urlpatterns = [
    path("", LeadersView.as_view(), name="leaders"),

    path("all/", RedirectView.as_view(url="/leaders"), name="all"),

    # Classic.
    path(
        "classic/",
        LeadersView.as_view(game_type=GameType.CLASSIC),
        name="classic"
    ),

    # Dead/Living.
    # TODO: Find a way to display these.
    # path("dead/", LeadersView.as_view(deleted=1), name="dead"),
    # path("living/", LeadersView.as_view(deleted=0), name="living"),

    # Survival.
    path(
        "survival/",
        LeadersView.as_view(game_type=GameType.SURVIVAL),
        name="survival"
    ),
    path(
        "survival/dead/",
        LeadersView.as_view(game_type=GameType.SURVIVAL, deleted=1),
        name="dead_survival"
    ),
    path(
        "survival/living/",
        LeadersView.as_view(game_type=GameType.SURVIVAL, deleted=0),
        name="living_survival"
    ),

    # Hardcore.
    path(
        "hardcore/",
        LeadersView.as_view(game_type=GameType.HARDCORE),
        name="hardcore"
    ),
    path(
        "hardcore/dead/",
        LeadersView.as_view(game_type=GameType.HARDCORE, deleted=1),
        name="dead_hardcore"
    ),
    path(
        "hardcore/living/",
        LeadersView.as_view(game_type=GameType.HARDCORE, deleted=0),
        name="living_hardcore"
    )
]
