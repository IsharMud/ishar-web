from rest_framework.serializers import ModelSerializer

from .models import Patch


class PatchSerializer(ModelSerializer):
    class Meta:
        model = Patch
        fields = "__all__"
