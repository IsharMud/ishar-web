"""Time delta handling"""
def stringify(delta=None):
    """Stringify time deltas"""
    try:

        # Less than a day
        if delta.days < 1:

            # A minute or more
            if delta.seconds >= 60:
                minutes = int(delta.seconds / 60)

                # An hour or more
                if minutes >= 60:
                    hours = int(minutes / 60)
                    if hours >= 1:
                        ret = { 'value': hours, 'interval': 'hour'}
                    else:
                        ret = { 'value': minutes, 'interval': 'minute'}
                else:
                    ret = { 'value': minutes, 'interval': 'minute'}
            else:
                ret = { 'value': delta.seconds, 'interval': 'second'}

        # Less than a month
        elif delta.days < 30:
            hours   = int(delta.seconds // (60 * 60))
            minutes = int((delta.seconds // 60) % 60)
            return f"{delta.days}d {hours}h {minutes}m"

        # At least a month
        elif delta.days >= 30:
            months  = int(delta.days / 30)

            # A year or more
            if months >= 12:
                years   = int(months / 12)

                # A decade or more
                if years >= 10:
                    decades = int(years / 10)
                    ret = { 'value': decades, 'interval': 'decade'}
                else:
                    ret = { 'value': years, 'interval': 'year'}
            else:
                ret = { 'value': months, 'interval': 'month'}
        else:
            return str(delta)

        # Append "s", if not singular
        if ret and ret['value'] != 1:
            ret['interval'] += 's'

        return f"{ret['value']} {ret['interval']}"

    except Exception as err:
        print(err)
        return str(delta)
