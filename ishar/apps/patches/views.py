from django.views.generic import ListView
from rest_framework import viewsets, permissions

from .models import Patch
from .serializers import PatchSerializer


class PatchAllView(ListView):
    context_object_name = "patches"
    model = Patch
    template_name = "patches.html.djt"


class PatchListView(PatchAllView):
    paginate_by = 3


class PatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows players to be viewed.
    """
    model = Patch
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PatchSerializer
