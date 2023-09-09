from django.utils.timezone import now

from .models import GlobalEvent


def get_global_event_count():
    """
    Number of current global events within the MUD.
    """
    event_count = GlobalEvent.objects.filter(
        start_time__lt=now(),
        end_time__gt=now()
    ).count()
    return event_count
