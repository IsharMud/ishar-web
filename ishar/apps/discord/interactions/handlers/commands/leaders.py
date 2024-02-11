from django.urls import reverse


def leaders(request):
    """Link to leaders page."""
    return ":trophy: <%s://%s%s>" % (
        request.scheme, request.get_host(), reverse("leaders")
    )
