from rest_framework import viewsets, permissions

from ..models import Account
from ..models.upgrade import AccountUpgrade
from ..serializers import AccountSerializer, AccountUpgradeSerializer


class AccountAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    model = Account
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()


class AccountUpgradeAPIVIewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    model = AccountUpgrade
    serializer_class = AccountUpgradeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
