"""
Ishar MUD API configuration.
"""

from rest_framework import permissions, routers

from .apps.account.views import AccountViewSet, AccountUpgradeViewSet
from .apps.challenge.views import ChallengeViewSet
from .apps.news.views import NewsViewSet
from .apps.patches.views import PatchViewSet
from .apps.player.views import PlayerViewSet, PlayerClassViewSet, RaceViewSet, \
    RemortUpgradeViewSet
from .apps.quest.views.api import QuestViewSet, QuestRewardViewSet, \
    QuestStepViewSet
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
api_router.register(r"accounts", AccountViewSet, "account")
api_router.register(r"account_upgrades", AccountUpgradeViewSet, "account_upgrade")
api_router.register(r"challenges", ChallengeViewSet, "challenge")
api_router.register(r"classes", PlayerClassViewSet, "class")
api_router.register(r"forces", ForceViewSet, "force")
api_router.register(r"news", NewsViewSet, "news")
api_router.register(r"patches", PatchViewSet, "patch")
api_router.register(r"players", PlayerViewSet, "player")
api_router.register(r"quests", QuestViewSet, "quest")
api_router.register(r"quest_rewards", QuestRewardViewSet, "quest_reward")
api_router.register(r"quest_steps", QuestStepViewSet, "quest_step")
api_router.register(r"races", RaceViewSet, "race")
api_router.register("remort_upgrades", RemortUpgradeViewSet, "remort_upgrade")
api_router.register(r"seasons", SeasonViewSet, "season")
api_router.register(r"spells", SpellViewSet, "spell")
api_router.register(r"spell_flags", SpellFlagViewSet, "spell_flag")
