from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, TemplateView

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


class IsharLoginView(LoginView):
    template_name = "login.html.djt"


class IsharLogoutView(LogoutView):
    template_name = "logout.html.djt"


class PortalView(LoginView):
    template_name = "portal.html.djt"

