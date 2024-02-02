from django.utils.timesince import timeuntil
from django.utils.timezone import now

from ishar.apps.events.models import GlobalEvent

from ..response import respond


def events() -> respond:
    """List any active global events."""

    # Find the global active events in the database.
    global_events = GlobalEvent.objects.filter(
        start_time__lt=now(),
        end_time__gt=now()
    ).all()

    # Proceed if there are any active events.
    if global_events.count() > 0:
        reply = "%i events:\n" % (global_events.count())

        # List the number, description, time left, and expiration of the event.
        for (num, event) in enumerate(global_events.all(), start=1):
            reply += "%i. %s - ends %s :alarm_clock: %s.\n" % (
                num,
                event.event_desc,
                timeuntil(event.end_time),
                event.end_time.strftime("%c %Z")
            )

        return respond(reply)

    # Say so if there are no active events.
    return respond("Sorry - no events right now.")
