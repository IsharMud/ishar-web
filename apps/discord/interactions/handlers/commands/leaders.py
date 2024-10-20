from django.urls import reverse


def leaders(request):
    # Link to leaders page.
    return (
        ":trophy: "
        f"[Leaders](<{request.scheme}://{request.get_host()}"
        f'{reverse("leaders")}#leaders>)'
    )
