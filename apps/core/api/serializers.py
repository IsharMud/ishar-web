from rest_framework.serializers import ModelSerializer


class BaseAPIModelSerializer(ModelSerializer):
    """Base Django-Rest-Framework (DRF) API model serializer."""
    class Meta:
        fields = "__all__"
