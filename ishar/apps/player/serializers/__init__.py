from rest_framework import serializers

from ..models import Player, PlayerClass


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class PlayerClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerClass
        fields = "__all__"
