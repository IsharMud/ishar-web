"""
isharmud.com patch utility functions.
"""


def sizeof_fmt(num=None, suffix='B'):
    """
    Convert bytes to human-readable file size.
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'
