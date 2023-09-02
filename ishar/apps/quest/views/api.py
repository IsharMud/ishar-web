from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from ..models import Quest
from ..models.reward import QuestReward
from ..models.step import QuestStep
from ..serializers import (
    QuestSerializer, QuestRewardSerializer, QuestStepSerializer
)


class QuestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quests to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    model = Quest
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = QuestSerializer


class QuestRewardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quest rewards to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    model = QuestReward
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = QuestRewardSerializer


class QuestStepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quest steps to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    model = QuestStep
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = QuestStepSerializer
