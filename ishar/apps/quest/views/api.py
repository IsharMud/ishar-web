from rest_framework import viewsets, permissions

from ..models import Quest
from ..models.reward import QuestReward
from ..models.step import QuestStep
from ..serializers import (
    QuestSerializer, QuestRewardSerializer, QuestStepSerializer
)


class QuestAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quests to be viewed or edited.
    """
    model = Quest
    serializer_class = QuestSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Quest.objects.all()


class QuestRewardAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quest rewards to be viewed or edited.
    """
    model = QuestReward
    serializer_class = QuestRewardSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = QuestReward.objects.all()


class QuestStepAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quest steps to be viewed or edited.
    """
    model = QuestStep
    serializer_class = QuestStepSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = QuestStep.objects.all()
