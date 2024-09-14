from django.utils.timezone import now


def mudtime():
    """Show the current server (UTC) time."""
    time = now().strftime("%A, %B %d, %Y @ %I:%M:%S %p %Z")
    return f"{time} :clock:"
