from rest_framework.serializers import ModelSerializer

from ..models import Account
from ..models.upgrade import AccountUpgrade


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class AccountUpgradeSerializer(ModelSerializer):
    class Meta:
        model = AccountUpgrade
        fields = "__all__"
