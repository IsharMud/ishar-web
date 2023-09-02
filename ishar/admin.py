from django.contrib import admin
from django.contrib.auth.admin import Group

# Disable "groups" in /admin/
admin.site.unregister(Group)
