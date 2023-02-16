"""Time delta handling"""


def pluralize(timing=None):
    """Append "s" and stringifies time-deltas, if not singular"""
    if round(timing['value']) != 1:
        timing['interval'] += 's'

    # Round the number in the output string
    return f"{round(timing['value'])} {timing['interval']}"


def stringify(delta=None):
    """Stringify time deltas"""

    # Process days
    if delta.days:

        # Calculate years
        if delta.days >= 365:
            value = delta.days / 365
            interval = 'year'

        # Calculate months
        elif delta.days >= 30:
            value = delta.days / 30
            interval = 'month'

        # Calculate weeks
        elif delta.days >= 7:
            value = delta.days / 7
            interval = 'week'

        # Days require no math
        else:
            value = delta.days
            interval = 'day'

    # Calculate hours
    elif delta.seconds >= 3600:
        value = delta.seconds / 3600
        interval = 'hour'

    # Calculate minutes
    elif delta.seconds >= 60:
        value = delta.seconds / 60
        interval = 'minute'

    # Seconds require no math
    else:
        value = delta.seconds
        interval = 'second'

    # Make the output plural, if necessary
    return pluralize(
        timing={
            'value': value,
            'interval': interval
        }
    )
