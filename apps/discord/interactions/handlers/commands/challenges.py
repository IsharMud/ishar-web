from django.urls import reverse


def challenges(request):
    # Link to challenges page.
    return (
        f':crossed_swords: [Challenges]'
        f'(<{request.scheme}://{request.get_host()}'
        f'{reverse("challenges")}#challenges>)'
    )
