import ipaddress

from django.core.serializers import serialize


def dec2ip(value=None):
    """
    Convert IP address from decimal format to string.
    """
    if value:
        try:
            return ipaddress.ip_address(int(value))
        except ValueError:
            return value
    return None


def json_context(context=None, obj=None):
    """
    Include serialized content in response context.
    """
    qs = context.get(obj)
    if qs:
        context[obj] = serialize(format="json", queryset=qs)
    return context
