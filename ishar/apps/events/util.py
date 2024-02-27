from django.utils.timezone import now

from .models.event import GlobalEvent


def get_global_event_count():
    """
    Number of current, active global events within the MUD.
    """
    return GlobalEvent.objects.filter(
        start_time__lt=now(),
        end_time__gt=now()
    ).count()
