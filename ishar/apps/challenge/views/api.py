from rest_framework import viewsets, permissions

from ..models import Challenge
from ..serializers import ChallengeSerializer


class ChallengeAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows challenges to be viewed or edited.
    """
    model = Challenge
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Challenge.objects.all()
