from django.conf import settings
from pprint import pprint
from apps.leaders.models.leader import Leader
from apps.players.models.game_type import GameType


def leader(request, interaction=None):
    find_game_type = interaction["options"][0].get("value")
    qs = Leader.objects
    game_type_label = settings.WEBSITE_TITLE
    find_game_type = int(find_game_type)
    pprint(find_game_type)
    game_type = GameType._value2member_map_[find_game_type]
    pprint(game_type)
    qs = qs.filter(game_type__exact=game_type.value)
    game_type_label = game_type.label
    pprint(game_type_label)
    lead_player = qs.first()
    return (
        f':trophy: {lead_player.name} is the current {game_type_label} leader!'
    )
