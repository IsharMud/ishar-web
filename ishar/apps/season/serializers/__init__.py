from rest_framework import serializers

from ..models import Season


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"
