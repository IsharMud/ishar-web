"""
Ishar MUD API configuration.
"""

from rest_framework import permissions, routers

from ishar.apps.accounts.views import AccountsViewSet, AccountUpgradesViewSet
from ishar.apps.challenges.views import ChallengesViewSet
from ishar.apps.classes.views import ClassesViewSet
from ishar.apps.events.views import GlobalEventsViewSet
from ishar.apps.news.views import NewsViewSet
from ishar.apps.patches.views import PatchesViewSet
from ishar.apps.players.views import (
    PlayerViewSet, PlayerFlagViewSet, RemortUpgradesViewSet
)
from ishar.apps.quests.views import (
    QuestsViewSet, QuestPrereqsViewSet, QuestRewardsViewSet, QuestStepsViewSet
)
from ishar.apps.races.views import (
    RacesViewSet, RacesAffinityViewSet, RaceDeathloadViewSet, RacesSkillViewSet
)
from ishar.apps.seasons.views import SeasonViewSet
from ishar.apps.skills.views import (
    ForcesViewSet, SkillsViewSet, SpellFlagsViewSet, SkillsFlagsViewSet
)


class IsharMUDAPIView(routers.APIRootView):
    """
    Ishar MUD API view.
    """
    name = "Ishar MUD API"
    permission_classes = [permissions.IsAdminUser]
    pass


class IsharMUDAPIRouter(routers.DefaultRouter):
    """
    Ishar MUD API router.
    """
    APIRootView = IsharMUDAPIView


api_router = IsharMUDAPIRouter()
api_router.register(r"accounts", AccountsViewSet, "account")
api_router.register(r"account_upgrades", AccountUpgradesViewSet, "account_upgrade")
api_router.register(r"challenges", ChallengesViewSet, "challenge")
api_router.register(r"classes", ClassesViewSet, "class")
api_router.register(r"events", GlobalEventsViewSet, "event")
api_router.register(r"forces", ForcesViewSet, "force")
api_router.register(r"news", NewsViewSet, "news")
api_router.register(r"patches", PatchesViewSet, "patch")
api_router.register(r"players", PlayerViewSet, "player")
api_router.register(r"player_flags", PlayerFlagViewSet, "player_flag")
api_router.register(r"quests", QuestsViewSet, "quest")
api_router.register(r"quest_prereqs", QuestPrereqsViewSet, "quest_prereq")
api_router.register(r"quest_rewards", QuestRewardsViewSet, "quest_reward")
api_router.register(r"quest_steps", QuestStepsViewSet, "quest_step")
api_router.register(r"races", RacesViewSet, "race")
api_router.register(r"races_affinities", RacesAffinityViewSet, "race_affinity")
api_router.register(r"races_deathloads", RaceDeathloadViewSet, "race_deathload")
api_router.register(r"races_skills", RacesSkillViewSet, "race_skill")
api_router.register("remort_upgrades", RemortUpgradesViewSet, "remort_upgrade")
api_router.register(r"seasons", SeasonViewSet, "season")
api_router.register(r"skills", SkillsViewSet, "skill")
api_router.register(r"spell_flags", SpellFlagsViewSet, "spell_flag")
api_router.register(r"skills_flags", SkillsFlagsViewSet, "skills_flag")
