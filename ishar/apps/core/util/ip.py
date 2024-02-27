from ipaddress import ip_address


def dec2ip(value=None):
    """Convert IP address from decimal format to string."""
    if value:
        try:
            return ip_address(int(value))
        except ValueError:
            return value
    return None
