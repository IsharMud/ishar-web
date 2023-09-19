from rest_framework.serializers import ModelSerializer

from .models import Player, PlayerFlag, RemortUpgrade


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class PlayerFlagSerializer(ModelSerializer):
    class Meta:
        model = PlayerFlag
        fields = "__all__"


class RemortUpgradeSerializer(ModelSerializer):
    class Meta:
        model = RemortUpgrade
        fields = "__all__"
