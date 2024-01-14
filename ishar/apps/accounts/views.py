from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.base import TemplateView

from rest_framework import viewsets, permissions

from ishar.apps.accounts.models.upgrade import (
    AccountUpgrade, AccountAccountUpgrade
)
from ishar.apps.accounts.serializers import (
    AccountSerializer, AccountUpgradeSerializer, AccountAccountUpgradeSerializer
)


class AccountsViewSet(viewsets.ModelViewSet):
    """
    Read-only API endpoint that allows accounts to be viewed.
    """
    model = get_user_model()
    lookup_field = "account_id"
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


class AccountsUpgradesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows upgrades to accounts to be viewed or edited.
    """
    model = AccountAccountUpgrade
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = AccountAccountUpgradeSerializer


class PortalView(LoginRequiredMixin, TemplateView):
    template_name = "portal.html"


class PasswordView(LoginRequiredMixin, PasswordChangeView):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = "password.html"
