from django.urls import reverse

from apps.leaders.models.leader import Leader


def leaders(request):
    """Link to leaders page."""
    return (
        ':trophy: '
        f'<{request.scheme}://{request.get_host()}{reverse("leaders")}#leaders>'
    )
