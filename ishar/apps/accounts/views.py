from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.base import TemplateView

from rest_framework import viewsets, permissions

from .models.upgrade import AccountUpgrade
from .serializers import AccountSerializer, AccountUpgradeSerializer


class AccountsViewSet(viewsets.ReadOnlyModelViewSet):
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


class PortalView(LoginRequiredMixin, TemplateView):
    template_name = "portal.html.djt"


class AccountView(PortalView):
    template_name = "account.html.djt"


class PasswordView(LoginRequiredMixin, PasswordChangeView):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = "password.html.djt"
