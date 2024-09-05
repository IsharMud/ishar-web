from django.urls import reverse


def challenges(request):
    """Link to challenges page."""
    return ":crossed_swords: <%s://%s%s#%s>" % (
        request.scheme, request.get_host(), reverse("challenges"), "challenges"
    )
