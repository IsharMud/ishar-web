from django.utils.timezone import now

from ..response import respond


def mudtime() -> respond:
    """Show the current server (UTC) time."""
    return respond("%s :clock:" % (now()))
