from rest_framework.serializers import ModelSerializer

from .models import Challenge


class ChallengesSerializer(ModelSerializer):
    class Meta:
        model = Challenge
        fields = "__all__"
