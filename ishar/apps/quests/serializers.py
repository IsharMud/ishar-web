from rest_framework.serializers import ModelSerializer

from ishar.apps.quests.models import Quest, QuestPrereq, QuestReward, QuestStep


class QuestSerializer(ModelSerializer):
    class Meta:
        model = Quest
        fields = "__all__"


class QuestPrereqSerializer(ModelSerializer):
    class Meta:
        model = QuestPrereq
        fields = "__all__"


class QuestStepSerializer(ModelSerializer):
    class Meta:
        model = QuestStep
        fields = "__all__"


class QuestRewardSerializer(ModelSerializer):
    class Meta:
        model = QuestReward
        fields = "__all__"
