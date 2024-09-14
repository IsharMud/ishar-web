from django.urls import reverse


def faq(request):
    """Link to frequently asked questions page."""
    return (
        f':question:'
        f' {request.scheme}://{request.get_host()}{reverse("faq")}#faq'
    )
