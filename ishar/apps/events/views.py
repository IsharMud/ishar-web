from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic.list import ListView

from ishar.apps.events.models import GlobalEvent


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
