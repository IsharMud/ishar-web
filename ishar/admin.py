from django.contrib import admin
from django.contrib.auth.admin import Group


# Set header and title text for /admin/
admin.site.site_header = admin.site.site_title = "Ishar MUD"
admin.site.index_title = "Administration"

# Disable "groups" in /admin/
admin.site.unregister(Group)
