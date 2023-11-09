from rest_framework.serializers import ModelSerializer

from ishar.apps.clients.models import MUDClientCategory, MUDClient


class MUDClientCategorySerializer(ModelSerializer):
    class Meta:
        model = MUDClientCategory
        fields = "__all__"


class MUDClientSerializer(ModelSerializer):
    class Meta:
        model = MUDClient
        fields = "__all__"
