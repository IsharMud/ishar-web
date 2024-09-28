from django.conf import settings
from pprint import pprint
from apps.leaders.models import Leader


def leader(request, interaction=None):
    pprint(interaction["options"])
    find_game_type = interaction["options"][0].get("value")
    qs = Leader.objects
    game_type_name = settings.WEBSITE_TITLE
    if find_game_type:
        game_type_name = GameType._value2member_map_[find_game_type].label
        qs.filter(game_type__exact=find_game_type)
    lead_player = qs.order_by(
        "-remorts",
        "-statistics__total_renown",
        "-statistics__total_challenges",
        "-statistics__total_quests",
        "statistics__total_deaths",
        "-common__level"
    ).first()
    return (
        f':trophy: {lead_player.name} is the current {game_type_name} leader!'
    )
