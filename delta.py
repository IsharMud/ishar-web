"""Time delta handling"""

def pluralish(input=0):
    """Append "s" to stringified timedeltas, if not singular"""
    if input['value'] != 1:
        input['interval'] += 's'
    return f"{input['value']} {input['interval']}"

def stringify(delta=None):
    """Stringify time deltas"""
    delta_seconds   = delta.total_seconds()
    if delta_seconds < 60:
        ret = { 'value': delta_seconds, 'interval': 'second'}
    elif delta_seconds >= 60 and delta_seconds < 3600:
        ret = { 'value': int(delta_seconds / 60), 'interval': 'minute'}
    elif delta_seconds >= 3600 and delta.days < 1:
        ret = { 'value': int(delta_seconds / 3600), 'interval': 'hour'}
    elif delta.days >= 1 and delta.days < 7:
        ret = { 'value': delta.days, 'interval': 'day'}
    elif delta.days >= 7 and delta.days < 30:
        ret = { 'value': int(delta.days / 7), 'interval': 'week'}
    elif delta.days >= 30 and delta.days < 365:
        ret = { 'value': int(delta.days / 30), 'interval': 'month'}
    elif delta.days >= 365:
        ret = { 'value': int(delta.days / 365), 'interval': 'year'}
    else:
        return str(delta)
    return pluralish(ret)
