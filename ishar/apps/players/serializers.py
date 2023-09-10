from rest_framework.serializers import ModelSerializer

from .models import Player
from .models.classes import Class
from .models.race import Race
from .models.remort import RemortUpgrade


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class ClassSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"


class RaceSerializer(ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"


class RemortUpgradeSerializer(ModelSerializer):
    class Meta:
        model = RemortUpgrade
        fields = "__all__"
