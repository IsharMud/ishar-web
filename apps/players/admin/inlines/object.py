from django.contrib.admin import display, TabularInline
from django.urls import reverse
from django.utils.html import format_html

from apps.players.models.object import PlayerObject


class PlayerObjectsInlineAdmin(TabularInline):
    """Player's objects inline administration."""

    model = PlayerObject
    fields = readonly_fields = (
        "object", "position_type", "position_val", "get_container_link",
        "enchant", "timer", "state", "bound", "min_level",
        "val0", "val1", "val2", "val3"
    )
    verbose_name = "Object"

    @display(description="Container")
    def get_container_link(self, obj) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                viewname="admin:objects_object_change",
                args=(obj.parent_player_object.object.pk,)
            ),
            obj.parent_player_object.object
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
