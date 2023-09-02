from rest_framework import serializers

from ..models import Account
from ..models.upgrade import AccountUpgrade


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class AccountUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUpgrade
        fields = "__all__"
