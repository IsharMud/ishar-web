from rest_framework.serializers import ModelSerializer

from ishar.apps.patches.models import Patch


class PatchSerializer(ModelSerializer):
    class Meta:
        model = Patch
        fields = "__all__"
