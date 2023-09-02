from rest_framework import viewsets, permissions

from ..models import Account
from ..models.upgrade import AccountUpgrade
from ..serializers import AccountSerializer, AccountUpgradeSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows accounts to be viewed.
    """
    lookup_field = "account_name"
    model = Account
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = AccountSerializer


class AccountUpgradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows account upgrades to be viewed or edited.
    """
    model = AccountUpgrade
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = AccountUpgradeSerializer
