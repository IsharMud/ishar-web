from django.contrib import admin

from ..models.race import Race

from .inlines.affinity import RaceAffinityAdminInline
from .inlines.deathload import RaceDeathloadAdminInline
from .inlines.skill import RaceSkillAdminInline


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    """Race administration."""

    model = Race
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "race_id",
                    "display_name",
                    "symbol",
                    "folk_name"
                )
            }
        ),
        (
            "Descriptions",
            {
                "fields": (
                    "description",
                    "short_description",
                    "long_description",
                )
            },
        ),
        (
            "Defaults",
            {
                "fields": (
                    "default_movement",
                    "default_height",
                    "default_weight",
                )
            },
        ),
        (
            "Bonus",
            {
                "fields": (
                    "bonus_fortitude",
                    "bonus_reflex",
                    "bonus_resilience",
                    "listen_sound",
                    "height_bonus",
                    "weight_bonus",
                )
            },
        ),
        (
            "Attacks",
            {
                "fields": (
                    "attack_noun",
                    "attack_type"
                )
            }
        ),
        (
            "Additional Statistics",
            {
                "fields": (
                    "additional_str",
                    "additional_agi",
                    "additional_end",
                    "additional_per",
                    "additional_foc",
                    "additional_wil",
                )
            },
        ),
        (
            "Booleans",
            {
                "fields": (
                    "is_humanoid",
                    "is_invertebrae",
                    "is_flying",
                    "is_swimming",
                    "darkvision",
                    "see_invis",
                    "is_walking",
                    "endure_heat",
                    "endure_cold",
                    "is_undead",
                    "is_playable",
                )
            },
        ),
    )
    inlines = (
        RaceSkillAdminInline,
        RaceAffinityAdminInline,
        RaceDeathloadAdminInline
    )
    list_display = (
        "display_name",
        "symbol",
        "is_playable",
        "folk_name",
    )
    list_filter = ("is_playable",)
    readonly_fields = ("race_id",)
    search_fields = (
        "display_name",
        "symbol",
        "folk_name",
        "attack_noun",
        "description",
        "short_description",
        "long_description",
    )

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
