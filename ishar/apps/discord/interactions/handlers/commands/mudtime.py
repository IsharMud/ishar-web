from django.utils.timezone import now


def mudtime():
    """Show the current server (UTC) time."""
    return "%s :clock:" % (now())
