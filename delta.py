"""Time delta handling"""


def pluralize(timing=None):
    """Append "s" and stringifies time-deltas, if not singular"""
    if round(timing['value']) != 1:
        timing['interval'] += 's'

    # Round the number in the output string
    return f"{round(timing['value'])} {timing['interval']}"


def stringify(delta=None):
    """Stringify time deltas"""

    # Days require no math
    if delta.days:
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
