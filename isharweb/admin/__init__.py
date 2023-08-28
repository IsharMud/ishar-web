from django.contrib import admin
from django.contrib.auth.admin import Group

from .account import AccountAdmin
from .force import ForceAdmin
from .player import ClassAdmin, PlayerAdmin
from .quest import QuestAdmin, QuestStepAdmin
from .race import RaceAdmin
from .spell import SpellInfoAdmin

from ..models.account import Account
from ..models.force import Force
from ..models.player import Player, Class
from ..models.quest import Quest
from ..models.race import Race
from ..models.spell import SpellInfo


admin.site.register(Account, AccountAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Force, ForceAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Quest, QuestAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(SpellInfo, SpellInfoAdmin)

# Disable "groups" in /admin/
admin.site.unregister(Group)
