from django.contrib.admin import StackedInline

from ...models.room_exit import RoomExit


class RoomExitStackedInline(StackedInline):
    """Ishar room exit stacked inline administration."""

    model = RoomExit
    extra = 0
    fields = readonly_fields = (
        "id",
        "room_vnum",
        "exit_index",
        "destination_vnum",
        "exit_name",
        "door_name",
        "description",
        "key_vnum",
        "linked_exit_index",
        "size_restriction",
        "skill_modifier",
        "trap_type",
    )
    verbose_name = "Room Exit"
    verbose_name_plural = "Room Exits"


    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
