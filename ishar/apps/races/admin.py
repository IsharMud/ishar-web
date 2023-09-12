from django.contrib import admin

from .models import Race, RacialAffinity


@admin.register(Race)
class RacesAdmin(admin.ModelAdmin):
    """
    Ishar race administration.
    """
    model = Race
    fieldsets = (
        (None, {"fields": ("race_id", "display_name", "symbol", "folk_name")}),
        ("Descriptions", {"fields": ("short_description", "long_description")}),
        ("Defaults", {"fields": (
            "default_movement", "default_height", "default_weight"
        )}),
        ("Bonus", {"fields": (
            "bonus_fortitude", "bonus_reflex", "bonus_resilience",
            "listen_sound", "height_bonus", "weight_bonus"
        )}),
        ("Attacks", {"fields": ("attack_noun", "attack_type")}),
        ("Weaknesses", {"fields": ("vulnerabilities", "susceptibilities")}),
        ("Protections", {"fields": ("resistances", "immunities")}),
        ("Additional Statistics", {"fields": (
            "additional_str", "additional_agi", "additional_end",
            "additional_per", "additional_foc", "additional_wil"
        )}),
        ("Booleans", {"fields": (
            "is_humanoid", "is_invertebrae", "is_flying", "is_swimming",
            "darkvision", "see_invis", "is_walking",
            "endure_heat", "endure_cold", "is_undead", "is_playable"
        )}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = (
        "display_name", "symbol", "is_playable", "folk_name",
        "short_description"
    )
    list_filter = ("is_playable",)
    readonly_fields = ("race_id",)
    search_fields = (
        "display_name", "symbol", "folk_name", "attack_noun",
        "short_description", "long_description"
    )

    def has_add_permission(self, request, obj=None):
        return request.user.is_god()

    def has_change_permission(self, request, obj=None):
        return request.user.is_god()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_god()


@admin.register(RacialAffinity)
class RacialAffinitiesAdmin(admin.ModelAdmin):
    """
    Ishar race administration.
    """
    model = Race
    fieldsets = ((None, {"fields": ("race", "force", "affinity_type")}),)
    filter_horizontal = filter_vertical = ()
    list_display = ("race", "force", "affinity_type")
    list_filter = ("force", "affinity_type")
    readonly_fields = ()
    search_fields = ("race", "force", "affinity_type")

    def has_add_permission(self, request, obj=None):
        return request.user.is_god()

    def has_change_permission(self, request, obj=None):
        return request.user.is_god()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_god()
