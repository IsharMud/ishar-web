from rest_framework.routers import DefaultRouter

from apps.players.api.viewsets import PlayersViewSet


api_router = DefaultRouter()

api_router.register("players", PlayersViewSet)
