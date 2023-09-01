from rest_framework import serializers

from ..models import Quest
from ..models.reward import QuestReward
from ..models.step import QuestStep


class QuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quest
        fields = "__all__"


class QuestRewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestReward
        fields = "__all__"


class QuestStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestStep
        fields = "__all__"
