from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from .models.upgrade import AccountUpgrade
from .serializers import AccountSerializer, AccountUpgradeSerializer


class AccountsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows accounts to be viewed.
    """
    model = get_user_model()
    lookup_field = model.USERNAME_FIELD
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = AccountSerializer


class AccountUpgradesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows account upgrades to be viewed or edited.
    """
    model = AccountUpgrade
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = AccountUpgradeSerializer
