from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from ishar.apps.clients.models import MUDClientCategory, MUDClient
from ishar.apps.clients.serializers import (
    MUDClientCategorySerializer, MUDClientSerializer
)


class MUDClientCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows MUD client categories to be viewed or edited.
    """
    model = MUDClientCategory
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = MUDClientCategorySerializer


class MUDClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows MUD clients to be viewed or edited.
    """
    model = MUDClient
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = MUDClientSerializer


class MUDClientsView(ListView):
    """
    MUD Clients view.
    """
    context_object_name = "mud_client_categories"
    model = MUDClientCategory
    template_name = "clients.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_visible__exact=1)
