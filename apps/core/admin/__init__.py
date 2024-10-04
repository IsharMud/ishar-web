from django.conf import settings

from django.contrib import admin
from django.contrib.auth.admin import Group

from ..models.affect_flag import AffectFlag
from ..models.player_flag import PlayerFlag
from ..models.title import Title

from .affect_flag import AffectFlagAdmin
from .player_flag import PlayerFlagAdmin
from .title import TitleAdmin


# Set admin header and title text.
admin.site.site_header = admin.site.site_title = settings.WEBSITE_TITLE
admin.site.index_title = "Administration"

# Disable original admin Group model.
admin.site.unregister(Group)

# Register our core models.
admin.site.register(AffectFlag, AffectFlagAdmin)
admin.site.register(PlayerFlag, PlayerFlagAdmin)
admin.site.register(Title, TitleAdmin)
