from apps.core.api.viewsets import BaseAPIModelViewSet

from .serializers import PlayerModelSerializer

from ..models import Player


class PlayersViewSet(BaseAPIModelViewSet):
    """Django-Rest-Framework (DRF) Player API view-set."""
    model = Player
    queryset = model.objects
    serializer_class = PlayerModelSerializer
