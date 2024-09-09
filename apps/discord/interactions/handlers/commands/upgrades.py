from django.urls import reverse

def upgrades(request):
    """Link to remort upgrades page."""
    return ":shield: <%s://%s%s#%s>" % (
        request.scheme,
        request.get_host(),
        reverse("upgrades"),
        "upgrades"
    )
