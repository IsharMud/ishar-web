from django.contrib.admin import display, TabularInline
from django.urls import reverse
from django.utils.html import format_html

from apps.players.models.object import PlayerObject


class PlayerObjectsInlineAdmin(TabularInline):
    """Player's objects inline administration."""
    model = PlayerObject
    list_display = ("get_object_link",)
    verbose_name = "Object"
    verbose_name_plural = "Objects"

    @display(description="Object", ordering="object__longname")
    def get_object_link(self, obj) -> str:
        """Admin link for player flag."""
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                viewname="admin:objects_object_change",
                args=(obj.object,)
            ),
            obj.object.longname or obj.object.name
        )

    def has_add_permission(self, request, obj) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False
