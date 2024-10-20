from django.urls import reverse


def feedback(request):
    # Link to feedback page.
    return (
        ":postbox: [Feedback]"
        f'(<{request.scheme}://{request.get_host()}{reverse("feedback")}#feedback>)'
    )
