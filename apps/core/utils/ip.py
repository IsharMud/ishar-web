"""IPv4 helpers for the game's ``haddr`` columns.

The game stores addresses as *signed* 32-bit host-order integers (the C
binds ``int`` via ``MYSQL_TYPE_LONG``), so addresses at or above 128.0.0.0
appear negative in the database. Both directions here honor that.
"""
from ipaddress import IPv4Address, ip_address


def dec2ip(value=None):
    if not value:
        return None
    try:
        return ip_address(int(value) & 0xFFFFFFFF)
    except ValueError:
        return value


def ip2dec(value=None):
    if not value:
        return 0
    try:
        as_int = int(IPv4Address(value))
    except ValueError:
        return 0
    return as_int - 2**32 if as_int >= 2**31 else as_int


def client_ip(request):
    """The requesting client's IPv4 address, or None.

    Behind the host proxy the client arrives in X-Forwarded-For; the first
    hop is the client. Falls back to REMOTE_ADDR (the proxy itself) and to
    None for non-IPv4 (IPv6 has no haddr representation).
    """
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    candidate = (
        forwarded.split(",")[0].strip()
        if forwarded else request.META.get("REMOTE_ADDR", "")
    )
    try:
        IPv4Address(candidate)
    except ValueError:
        return None
    return candidate
