from rest_framework.serializers import ModelSerializer

from ..models import Quest
from ..models.reward import QuestReward
from ..models.step import QuestStep


class QuestSerializer(ModelSerializer):
    class Meta:
        model = Quest
        fields = "__all__"


class QuestRewardSerializer(ModelSerializer):
    class Meta:
        model = QuestReward
        fields = "__all__"


class QuestStepSerializer(ModelSerializer):
    class Meta:
        model = QuestStep
        fields = "__all__"
