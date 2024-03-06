from django.conf import settings

from django.contrib import admin
from django.contrib.auth.admin import Group

from .affect_flag import AffectFlagAdmin
from .player_flag import PlayerFlagAdmin
from .process import MUDProcessAdmin


# Set header and title text for /admin/
admin.site.site_header = admin.site.site_title = settings.WEBSITE_TITLE
admin.site.index_title = "Administration"

# Disable "groups" in /admin/
admin.site.unregister(Group)
