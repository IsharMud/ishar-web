from .utils import get_global_event_count


def global_event_count(request):
    # Context processor for number of current global events within the MUD.
    return {"GLOBAL_EVENT_COUNT": get_global_event_count()}
