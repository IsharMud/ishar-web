from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.views.generic.list import ListView

from .models.event import GlobalEvent


class GlobalEventsView(LoginRequiredMixin, ListView):
    """
    Global events view.
    """
    context_object_name = "global_events"
    model = GlobalEvent
    template_name = "events.html"

    def get_queryset(self):
        current = now()
        return super().get_queryset().filter(
            start_time__lt=current,
            end_time__gt=current
        )
