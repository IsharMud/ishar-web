from django.contrib import admin
from django.contrib.auth.admin import Group


# Set header and title text for /admin/
admin.site.site_header = "IsharMUD Administration"
admin.site.site_title = "Administration Portal"
admin.site.index_title = "Portal"

# Disable "groups" in /admin/
admin.site.unregister(Group)
