from rest_framework import viewsets, permissions

from ..models import Challenge
from ..serializers import ChallengeSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows challenges to be viewed or edited.
    """
    model = Challenge
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = ChallengeSerializer
