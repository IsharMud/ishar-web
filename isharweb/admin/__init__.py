from django.contrib import admin
from django.contrib.auth.admin import Group

from .account import AccountAdmin
from .player import PlayerAdmin
from .quest import QuestAdmin, QuestStepAdmin

from ..models.account import Account
from ..models.player import Player

from ..models.quest import Quest
from ..models.quest.step import QuestStep


admin.site.register(Account, AccountAdmin)
admin.site.register(Player, PlayerAdmin)

admin.site.register(Quest, QuestAdmin)
# admin.site.register(QuestStep, QuestStepAdmin)

# Disable "groups" in /admin/
admin.site.unregister(Group)
