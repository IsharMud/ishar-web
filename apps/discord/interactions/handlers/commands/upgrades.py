from django.urls import reverse

def upgrades(request):
    """Link to remort upgrades page."""
    return (
        f':shield: <{request.scheme}://{request.get_host()}'
        f'{reverse("upgrades")}#upgrades>'
    )
