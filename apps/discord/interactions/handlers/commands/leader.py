from django.conf import settings
from pprint import pprint
from apps.leaders.models.leader import Leader
from apps.players.models.game_type import GameType


def leader(request, interaction=None):
    find_game_type = interaction["options"][0].get("value")
    pprint(interaction["options"])
    pprint(interaction["options"][0])
    qs = Leader.objects
    game_type_label = settings.WEBSITE_TITLE
    if find_game_type and find_game_type.isnumeric():
        find_game_type = int(find_game_type)
        pprint(find_game_type)
        game_type = GameType._value2member_map_[find_game_type]
        qs.filter(game_type__exact=game_type)
        game_type_label = game_type.label
    lead_player = qs.order_by(
        "-remorts",
        "-statistics__total_renown",
        "-statistics__total_challenges",
        "-statistics__total_quests",
        "statistics__total_deaths",
        "-common__level"
    ).first()
    return (
        f':trophy: {lead_player.name} is the current {game_type_label} leader!'
    )
