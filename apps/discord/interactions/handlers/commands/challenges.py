from django.urls import reverse


def challenges(request):
    """Link to challenges page."""
    return (
        ':crossed_swords:'
        f' <{request.scheme}://{request.get_host()}'
        f'{reverse("challenges")}#challenges>'
    )
