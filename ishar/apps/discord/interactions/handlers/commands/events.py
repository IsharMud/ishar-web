from django.urls import reverse
from django.utils.timesince import timeuntil
from django.utils.timezone import now

from ishar.apps.events.models import GlobalEvent


def events(request):
    """List any active global events."""

    # Default message assuming there are no active events.
    reply = "Sorry - no events right now."

    # Find the global active events in the database.
    global_events = GlobalEvent.objects.filter(
        start_time__lt=now(),
        end_time__gt=now()
    ).all()

    # Proceed if there are any active events.
    if global_events.count() > 0:
        events_url = "<%s://%s%s>" % (
            request.scheme, request.get_host(), reverse("events")
        )
        reply = "%i events:\n%s\n" % (global_events.count(), events_url)

        # List the number, description, time left, and expiration of the event.
        for (num, event) in enumerate(global_events.all(), start=1):
            reply += "%i. %s - ends %s :alarm_clock: %s.\n" % (
                num,
                event.event_desc,
                timeuntil(event.end_time),
                event.end_time.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
            )

    # Return the reply.
    return reply
