from django.contrib import admin
from django.contrib.auth.admin import Group

from .account import AccountAdmin
from .player import PlayerAdmin
from .quest import QuestAdmin
#from .race import RaceAdmin
from .spell import SpellInfoAdmin

from ..models.account import Account
from ..models.player import Player

from ..models.quest import Quest
# from ..models.quest.step import QuestStep

# from ..models.race import Race

from ..models.spell import SpellInfo


admin.site.register(Account, AccountAdmin)
admin.site.register(Player, PlayerAdmin)

admin.site.register(Quest, QuestAdmin)
# admin.site.register(QuestStep, QuestStepAdmin)

# admin.site.register(Race, RaceAdmin)

admin.site.register(SpellInfo, SpellInfoAdmin)

# Disable "groups" in /admin/
admin.site.unregister(Group)
