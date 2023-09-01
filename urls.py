"""
isharmud.com URL configuration.
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from ishar.apps.account.views.api import AccountAPIViewSet
from ishar.apps.challenge.views.api import ChallengeAPIViewSet
from ishar.apps.player.views.api import PlayerAPIViewSet, PlayerClassAPIViewSet
from ishar.apps.news.views.api import NewsAPIViewSet
from ishar.apps.quest.views.api import (
    QuestAPIViewSet, QuestRewardAPIViewSet, QuestStepAPIViewSet
)
from ishar.apps.race.views.api import RaceAPIViewSet
from ishar.apps.season.views.api import SeasonAPIViewSet
from ishar.apps.spell.views.api import ForceAPIViewSet, SpellAPIViewSet


# Django Rest Framework ("DRF") API router URLs
api_router = routers.DefaultRouter()
api_router.register(r"accounts", AccountAPIViewSet, "account")
api_router.register(r"challenges", ChallengeAPIViewSet, "challenge")
api_router.register(r"classes", PlayerClassAPIViewSet, "class")
api_router.register(r"forces", ForceAPIViewSet, "force")
api_router.register(r"news", NewsAPIViewSet, "news")
api_router.register(r"players", PlayerAPIViewSet, "player")
api_router.register(r"quests", QuestAPIViewSet, "quest")
api_router.register(r"quest_rewards", QuestAPIViewSet, "quest_reward")
api_router.register(r"quest_steps", QuestAPIViewSet, "quest_step")
api_router.register(r"races", RaceAPIViewSet, "race")
api_router.register(r"seasons", SeasonAPIViewSet, "season")
api_router.register(r"spells", SpellAPIViewSet, "spell")
api_router.register(r"spell_flags", SpellAPIViewSet, "spell_flag")


urlpatterns = [
    path("", include("ishar.urls"), name="ishar"),
    path("accounts/", include("django.contrib.auth.urls"), name="accounts"),
    path("admin/", admin.site.urls, name="admin"),
    path("api/", include(api_router.urls), name="api")
]
