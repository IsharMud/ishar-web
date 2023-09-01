from rest_framework import viewsets, permissions

from ..serializers import Account, AccountSerializer


class AccountAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    model = Account
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Account.objects.all()

