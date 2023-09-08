from rest_framework.serializers import ModelSerializer

from .models import Season


class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"
