from django.urls import reverse


def faq(request):
    # Link to frequently asked questions page.
    return (
        f":question: [Frequently Asked Questions]"
        f'(<{request.scheme}://{request.get_host()}{reverse("faq")}#faq>)'
    )
