from rest_framework.serializers import ModelSerializer

from .models import GlobalEvent


class GlobalEventSerializer(ModelSerializer):
    class Meta:
        model = GlobalEvent
        fields = "__all__"
