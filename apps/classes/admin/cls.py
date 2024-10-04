from django.contrib.admin import ModelAdmin

from .inlines.level import ClassLevelTabularInline
from .inlines.race import ClassRaceTabularInline
from .inlines.skill import ClassSkillTabularInline


class ClassAdmin(ModelAdmin):
    """Ishar class administration."""

    fieldsets = (
        (None, {"fields": (
            "class_id", "class_name", "class_display", "class_description",
            "is_playable"
        )}),
        ("Other", {"fields": ("attack_per_level", "spell_rate")}),
        ("Stat", {"fields": ("class_dc", "class_stat")}),
        ("Hit Points", {"fields": ("base_hit_pts", "hit_pts_per_level")}),
        ("Base", {"fields": (
            "base_fortitude", "base_resilience", "base_reflex"
        )}),
        ("Priority", {"fields": (
            "strength_priority", "agility_priority", "endurance_priority",
            "perception_priority", "focus_priority", "willpower_priority"
        )}),
    )
    inlines = (
        ClassLevelTabularInline,
        ClassRaceTabularInline,
        ClassSkillTabularInline
    )
    list_filter = ("is_playable",)
    list_display = list_display_links = (
        "class_id", "get_class_name", "is_playable"
    )
    ordering = ("-is_playable",)
    readonly_fields = ("class_id",)
    search_fields = ("class_name", "class_display", "class_description")

    def has_add_permission(self, request) -> bool:
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

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
