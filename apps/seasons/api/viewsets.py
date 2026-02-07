from apps.core.api.viewsets import BaseAPIModelViewSet

from .serializers import SeasonModelSerializer

from ..models import Season


class SeasonsViewSet(BaseAPIModelViewSet):
    """Django-Rest-Framework (DRF) Season API view-set."""
    model = Season
    queryset = model.objects
    serializer_class = SeasonModelSerializer
