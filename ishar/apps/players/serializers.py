from rest_framework.serializers import ModelSerializer

from ishar.apps.players.models import Player
from ishar.apps.players.models.flag import PlayerFlag, PlayersFlag
from ishar.apps.players.models.upgrade import RemortUpgrade, PlayerRemortUpgrade


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


class PlayersFlagSerializer(ModelSerializer):
    class Meta:
        model = PlayersFlag
        fields = "__all__"


class PlayerRemortUpgradeSerializer(ModelSerializer):
    class Meta:
        model = PlayerRemortUpgrade
        fields = "__all__"
