from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from ishar.apps.events.models import GlobalEvent
from ishar.apps.events.serializers import GlobalEventSerializer


class GlobalEventsView(LoginRequiredMixin, ListView):
    """
    Global events view.
    """
    context_object_name = "global_events"
    model = GlobalEvent
    queryset = model.objects.filter(
        start_time__lt=timezone.now(),
        end_time__gt=timezone.now()
    )
    template_name = "events.html"


class GlobalEventsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows global events to be viewed.
    """
    model = GlobalEvent
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = GlobalEventSerializer
