from apps.core.api.serializers import BaseAPIModelSerializer

from ..models import Season


class SeasonModelSerializer(BaseAPIModelSerializer):
    """Django-Rest-Framework (DRF) Season serializer."""
    class Meta:
        model = Season
        fields = "__all__"
