from django.utils.timesince import timeuntil
from django.utils.timezone import now
from django.utils.translation import ngettext

from apps.events.models import GlobalEvent

from .base import SlashCommand


class EventsCommand(SlashCommand):
    """List any active global events."""

    name = "events"
    ephemeral = True

    def handle(self) -> tuple[str, bool]:
        global_events = GlobalEvent.objects.filter(
            start_time__lt=now(),
            end_time__gt=now(),
        )
        num_events = global_events.count()

        if not num_events:
            return "Sorry - no events right now.", True

        label = ngettext(
            singular="event", plural="events", number=num_events,
        )
        events_link = self.site_link(
            f"{num_events} {label}", "events", fragment="events",
        )
        reply = f"{events_link}:\n"

        for num, event in enumerate(global_events, start=1):
            end = event.end_time.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
            reply += (
                f"{num}. {event.event_desc}"
                f" - ends {timeuntil(event.end_time)}"
                f" :alarm_clock: {end}.\n"
            )

        return reply, False
