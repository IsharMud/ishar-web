from django.urls import reverse

from apps.challenges.models import Challenge


def challenges(request, interaction=None):
    # Link to challenges, with counts of active, complete, and incomplete.
    challenges_url = f'{reverse("challenges")}#challenges'

    # TODO: use interaction.
    print("Discord Challenges interaction:", interaction)

    try:
        qs = Challenge.objects.filter(is_active__exact=1)
        num_active = qs.count()
        num_complete = qs.exclude(winner_desc__exact="").count()
        num_incomplete = qs.filter(winner_desc__exact="").count()
    except Challenge.DoesNotExist:
        num_active = num_complete = num_incomplete = 0

    return (
        f":crossed_swords: [Challenges]"
        f"(<{request.scheme}://{request.get_host()}{challenges_url}>) -"
        f" {num_active} active - {num_complete} complete /"
        f" {num_incomplete} incomplete."
    )
