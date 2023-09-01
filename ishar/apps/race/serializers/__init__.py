from rest_framework import serializers

from ..models import Race


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"
