from django.contrib.admin import ModelAdmin, register

from ishar.apps.players.models.flag import PlayerFlag


@register(PlayerFlag)
class PlayerFlagAdmin(ModelAdmin):
    """
    Player flag administration.
    """
    model = PlayerFlag
    fieldsets = ((None, {"fields": ("flag_id", "name")}),)
    list_display = list_display_links = search_fields = ("flag_id", "name",)
    readonly_fields = ("flag_id",)
    verbose_name = "Player's Flag"
    verbose_name_plural = "Player's Flags"
