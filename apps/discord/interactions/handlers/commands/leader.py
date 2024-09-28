from django.conf import settings
from pprint import pprint
from apps.leaders.models import Leader


def leader(request, interaction=None):
    pprint(interaction["options"])
    find_game_type = interaction["options"][0].get("value")
    qs = Leader.objects
    if find_game_type:
        qs.filter(game_type__exact=find_game_type)
    lead_player = qs.first()
    return (
        f':trophy: {lead_player.name} is the current'
        f' {find_game_type or settings.WEBSITE_TITLE} leader!'
    )
