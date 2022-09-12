def stringify(delta=None):
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
                        r = { 'value': hours, 'interval': 'hour'}
                    else:
                        r = { 'value': minutes, 'interval': 'minute'}
                else:
                    r = { 'value': minutes, 'interval': 'minute'}
            else:
                r = { 'value': delta.seconds, 'interval': 'second'}

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
                    r = { 'value': decades, 'interval': 'decade'}
                else:
                    r = { 'value': years, 'interval': 'year'}
            else:
                r = { 'value': months, 'interval': 'month'}
        else:
            return str(delta)

        # Append "s", if not singular
        if r and r['value'] != 1:
            r['interval'] += 's'

        return f"{r['value']} {r['interval']}"

    except Exception as e:
        print(e)
        return str(delta)
