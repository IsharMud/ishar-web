from django.urls import reverse

from apps.challenges.models import Challenge


def challenges(request):
    # Link to challenges, with counts of active, complete, and incomplete.
    icon = ":crossed_swords:"
    qs = Challenge.objects.filter(is_active__exact=1)

    base_url = f"{request.scheme}://{request.get_host()}"
    challenges_url = ("[Challenges]"
                      f"(<{base_url}{reverse('challenges')}#challenges>)")

    num_complete = qs.exclude(winner_desc__exact="").count()
    complete_url = f"{num_complete} complete"
    if num_complete:
        complete_url = (f"[{num_complete} complete]"
                        f"(<{base_url}{reverse('complete')}#complete>)")

    num_incomplete = qs.filter(winner_desc__exact="").count()
    incomplete_url = f"{num_incomplete} incomplete"
    if num_incomplete:
        incomplete_url = (f"[{num_incomplete} incomplete]"
                          f"(<{base_url}{reverse('incomplete')}#incomplete>)")

    return f"{challenges_url} {icon} {complete_url} - {incomplete_url}."
