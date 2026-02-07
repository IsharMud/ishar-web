from apps.core.api.serializers import BaseAPIModelSerializer

from ..models import Player


class PlayerModelSerializer(BaseAPIModelSerializer):
    """Django-Rest-Framework (DRF) Player serializer."""
    class Meta:
        model = Player
        fields = "__all__"
