from django.urls import reverse


def leaders(request):
    """Link to leaders page."""
    return (
        f':trophy: '
        f'<{request.scheme}://{request.get_host()}{reverse("leaders")}#leaders>'
    )
