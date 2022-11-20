"""Time delta handling"""


def pluralish(timing=None):
    """Append "s" to stringified timedeltas, if not singular"""
    if timing['value'] != 1:
        timing['interval'] += 's'

    # Round the number in the output string
    return f"{round(timing['value'])} {timing['interval']}"


def stringify(delta=None):
    """Stringify time deltas"""

    # Days require no math
    if delta.days:
        ret = {'value': delta.days, 'interval': 'day'}

    # Calculate hours
    elif delta.seconds >= 3600:
        ret = {'value': delta.seconds / 3600, 'interval': 'hour'}

    # Calculate minutes
    elif delta.seconds >= 60:
        ret = {'value': delta.seconds / 60, 'interval': 'minute'}

    # Seconds require no math
    else:
        ret = {'value': delta.seconds, 'interval': 'second'}

    return pluralish(timing=ret)
