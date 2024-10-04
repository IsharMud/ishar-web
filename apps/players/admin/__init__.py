from django.contrib.admin import site

from ..models.immortal import Immortal
from ..models.object import PlayerObject
from ..models.player import Player
from ..models.remort_upgrade import RemortUpgrade

from .immortal import ImmortalAdmin
from .object import PlayerObjectAdmin
from .player import PlayerAdmin
from .upgrade import RemortUpgradeAdmin


site.register(Immortal, ImmortalAdmin)
site.register(PlayerObject, PlayerObjectAdmin)
site.register(Player, PlayerAdmin)
site.register(RemortUpgrade, RemortUpgradeAdmin)
