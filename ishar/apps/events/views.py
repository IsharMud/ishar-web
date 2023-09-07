from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from .models import GlobalEvent
from .serializers import GlobalEventSerializer


class GlobalEventsView(ListView):
    """
    Global events view.
    """
    context_object_name = "global_events"
    model = GlobalEvent
    queryset = model.objects.all()
    template_name = "events.html.djt"


class GlobalEventsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows global events to be viewed.
    """
    model = GlobalEvent
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = GlobalEventSerializer
