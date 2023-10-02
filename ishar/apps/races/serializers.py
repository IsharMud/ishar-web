from rest_framework.serializers import ModelSerializer

from ishar.apps.races.models import Race


class RaceSerializer(ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"
