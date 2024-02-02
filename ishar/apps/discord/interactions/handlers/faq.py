from django.urls import reverse

from ..response import respond


def faq(request) -> respond:
    """Link to frequently asked questions page."""
    return respond(
        "%s://%s%s" % (request.scheme, request.get_host(), reverse("faq"))
    )
