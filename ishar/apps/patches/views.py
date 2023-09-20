from django.views.generic import ListView
from rest_framework import viewsets, permissions

from .models import Patch
from .serializers import PatchSerializer


class PatchesAllView(ListView):
    """
    Patches base list view of all patches.
    """
    context_object_name = "patches"
    model = Patch
    queryset = model.objects.filter(
        is_visible=True
    ).order_by(
        "-patch_date"
    ).all()
    template_name = "patches.html.djt"


class PatchesLatestView(PatchesAllView):
    model = Patch
    queryset = model.objects.filter(
        is_visible=True
    ).order_by(
        "-patch_date"
    ).all()[:1]


class PatchesListView(PatchesAllView):
    paginate_by = 5


class PatchesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows patches to be viewed.
    """
    model = Patch
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PatchSerializer
