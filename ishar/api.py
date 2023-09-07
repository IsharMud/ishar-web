"""
Ishar MUD API configuration.
"""

from rest_framework import permissions, routers

from .apps.accounts.views import AccountsViewSet, AccountUpgradesViewSet
from .apps.challenges.views import ChallengesViewSet
from .apps.events.views import GlobalEventsViewSet
from .apps.news.views import NewsViewSet
from .apps.patches.views import PatchViewSet
from .apps.player.views import PlayerViewSet, PlayerClassViewSet, RaceViewSet, \
    RemortUpgradeViewSet
from .apps.quests.views import QuestsViewSet, QuestPrereqsViewSet, \
    QuestRewardsViewSet, QuestStepsViewSet
from .apps.season.views import SeasonViewSet
from .apps.spell.views import ForceViewSet, SpellViewSet, SpellFlagViewSet


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
api_router.register(r"classes", PlayerClassViewSet, "class")
api_router.register(r"events", GlobalEventsViewSet, "event")
api_router.register(r"forces", ForceViewSet, "force")
api_router.register(r"news", NewsViewSet, "news")
api_router.register(r"patches", PatchViewSet, "patch")
api_router.register(r"players", PlayerViewSet, "player")
api_router.register(r"quests", QuestsViewSet, "quest")
api_router.register(r"quest_prereqs", QuestPrereqsViewSet, "quest_prereq")
api_router.register(r"quest_rewards", QuestRewardsViewSet, "quest_reward")
api_router.register(r"quest_steps", QuestStepsViewSet, "quest_step")
api_router.register(r"races", RaceViewSet, "race")
api_router.register("remort_upgrades", RemortUpgradeViewSet, "remort_upgrade")
api_router.register(r"seasons", SeasonViewSet, "season")
api_router.register(r"spells", SpellViewSet, "spell")
api_router.register(r"spell_flags", SpellFlagViewSet, "spell_flag")
