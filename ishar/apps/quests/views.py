from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .models import Quest, QuestPrereq, QuestStep, QuestReward
from .serializers import (
    QuestSerializer,
    QuestPrereqSerializer, QuestRewardSerializer, QuestStepSerializer
)


class QuestsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quests to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    model = Quest
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = QuestSerializer


class QuestPrereqsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quest prerequisites to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    model = QuestPrereq
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = QuestPrereqSerializer


class QuestRewardsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quest rewards to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    model = QuestReward
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = QuestRewardSerializer


class QuestStepsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quest steps to be viewed or edited.
    """
    filter_backends = [DjangoFilterBackend]
    model = QuestStep
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = QuestStepSerializer
