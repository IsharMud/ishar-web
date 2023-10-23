from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from ishar.apps.accounts.models.upgrade import (
    AccountUpgrade, AccountAccountUpgrade
)


class AccountSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class AccountUpgradeSerializer(ModelSerializer):
    class Meta:
        model = AccountUpgrade
        fields = "__all__"


class AccountAccountUpgradeSerializer(ModelSerializer):
    class Meta:
        model = AccountAccountUpgrade
        fields = "__all__"
