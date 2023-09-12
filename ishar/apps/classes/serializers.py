from rest_framework.serializers import ModelSerializer

from .models import Class


class ClassSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"
