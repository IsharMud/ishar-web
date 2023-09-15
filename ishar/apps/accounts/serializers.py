from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models.upgrade import AccountUpgrade


class AccountSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class AccountUpgradeSerializer(ModelSerializer):
    class Meta:
        model = AccountUpgrade
        fields = "__all__"
