from django.urls import reverse

from apps.challenges.models import Challenge


def challenges(request, interaction=None):
    # Link to challenges, with counts of active, complete, and incomplete.
    icon = ":crossed_swords:"

    # TODO: use interaction.
    print("Discord Challenges interaction:", interaction)

    qs = Challenge.objects.filter(is_active__exact=1)
    num_complete = qs.exclude(winner_desc__exact="").count()
    num_incomplete = qs.filter(winner_desc__exact="").count()

    anchor = "challenges"
    base_url = f"{request.scheme}://{request.get_host()}"
    challenges_url = (f"[Challenges]"
                      f"(<{base_url}{reverse(anchor)}#{anchor}>)")
    complete_url = (f"[{num_complete} complete]"
                    f"(<{base_url}{reverse('complete')}#{anchor}>)")
    incomplete_url = (f"[{num_incomplete} incomplete]"
                      f"(<{base_url}{reverse('incomplete')}#{anchor}>)")

    return f"{icon} {challenges_url} / {complete_url} - {incomplete_url}."
