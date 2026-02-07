from rest_framework.routers import DefaultRouter

from apps.players.api.viewsets import PlayersViewSet
from apps.seasons.api.viewsets import SeasonsViewSet


api_router = DefaultRouter()

api_router.register("players", PlayersViewSet)
api_router.register("seasons", SeasonsViewSet)
