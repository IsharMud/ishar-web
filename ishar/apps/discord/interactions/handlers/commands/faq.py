from django.urls import reverse


def faq(request):
    """Link to frequently asked questions page."""
    return "%s://%s%s" % (request.scheme, request.get_host(), reverse("faq"))
