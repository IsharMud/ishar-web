from django.urls import reverse
from django.utils.timesince import timeuntil
from django.utils.timezone import now
from django.utils.translation import ngettext

from apps.events.models.event import GlobalEvent


def events(request):
    """List any active global events."""

    # Default message assuming there are no active events.
    ephemeral = True
    reply = "Sorry - no events right now."

    # Find the global active events in the database.
    global_events = GlobalEvent.objects.filter(
        start_time__lt=now(),
        end_time__gt=now()
    ).all()

    # Proceed if there are any active events.
    num_events = global_events.count()
    if num_events and num_events > 0:
        ephemeral = False
        events_url = (
            f'{request.scheme}://{request.get_host()}{reverse("events")}#events'
        )
        reply = (
            f'{num_events} '
            f'{ngettext(singular="event", plural="events", number=num_events)}:'
            f' <{events_url}>\n'
        )

        # List the number, description, time left, and expiration of the event.
        for (num, event) in enumerate(global_events.all(), start=1):
            end = event.end_time.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
            reply += (
                f"{num}. {event.event_desc} - ends {timeuntil(event.end_time)}"
                f" :alarm_clock: {end}.\n"
            )

    # Return the reply.
    return reply, ephemeral
