from django.contrib import admin

from ..models.classes import PlayerClass


@admin.register(PlayerClass)
class PlayerClassAdmin(admin.ModelAdmin):
    """
    Ishar class administration.
    """
    fieldsets = ((None, {"fields": (
        "class_id", "class_name", "class_display", "class_description"
    )}),)
    filter_horizontal = filter_vertical = list_filter = ()
    readonly_fields = ("class_id",)
    list_display = search_fields = (
        "class_name", "class_display", "class_description"
    )
