from django.contrib.admin import ModelAdmin, register

from ..models.enigma import SeasonalEnigma


@register(SeasonalEnigma)
class SeasonalEnigmaAdmin(ModelAdmin):
    """Seasonal Enigma administration."""

    fieldsets = (
        (None, {"fields": ("seasonal_enigma_id", "enigma_name")}),
        ("Messages", {"fields": (
            "enigma_welcome", "enigma_intro_connect", "enigma_character_select"
        )})
    )
    list_display = list_display_links = ("seasonal_enigma_id", "enigma_name")
    readonly_fields = ("seasonal_enigma_id",)
    search_fields = (
        "enigma_name", "enigma_welcome", "enigma_intro_connect",
        "enigma_character_select"
    )

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
