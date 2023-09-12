from rest_framework.serializers import ModelSerializer

from .models import Race


class RaceSerializer(ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"
