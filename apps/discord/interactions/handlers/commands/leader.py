from django.conf import settings
from apps.leaders.models.leader import Leader
from apps.players.models.game_type import GameType


def leader(request, interaction=None):

    lead_label = settings.WEBSITE_TITLE
    qs = Leader.objects

    interaction_options = interaction.get("options")
    if interaction_options:
        find_game_type = interaction_options[0].get("value")
        game_type = GameType._value2member_map_[int(find_game_type)]
        qs = qs.filter(game_type__exact=game_type.value)
        lead_label = game_type.label

    lead_player = qs.first()
    return f':trophy: {lead_player.name} is the current {lead_label} leader!'
