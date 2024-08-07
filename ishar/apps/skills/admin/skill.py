from django.contrib import admin

from .inlines import (
    SkillComponentAdminInline, SkillModAdminInline, SkillForceAdminInline,
    SkillSpellFlagAdminInline
)

from ..models.skill import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Skill administration.
    """
    fieldsets = (
        (None, {"fields": (
            "id", "enum_symbol", "func_name", "skill_name", "skill_type"
        )}),
        ("Minimums", {"fields": ("min_posn", "min_use")}),
        ("Cost", {"fields": ("spell_breakpoint", "held_cost")}),
        ("Text", {"fields": (
                "wearoff_msg", "chant_text", "appearance", "decide_func",
                "obj_display"
        )}),
        ("Values", {"fields": ("difficulty", "rate", "notice_chance")}),
        ("Scale/Mod", {"fields": (
            "scale", "mod_stat_1", "mod_stat_2", "special_int"
        )}),
        ("Parent", {"fields": ("parent_skill",)})
    )
    inlines = (
        SkillComponentAdminInline,
        SkillForceAdminInline,
        SkillModAdminInline,
        SkillSpellFlagAdminInline,
    )
    list_display = ("skill_name", "skill_type")
    list_filter = (
        "skill_type",
        "min_posn",
        ("flag", admin.EmptyFieldListFilter),
        ("mod", admin.RelatedOnlyFieldListFilter),
        ("parent_skill", admin.RelatedOnlyFieldListFilter)
    )
    model = Skill
    ordering = ("-skill_type", "skill_name")
    radio_fields = {
        "min_posn": admin.HORIZONTAL,
        "skill_type": admin.HORIZONTAL,
    }
    readonly_fields = ("id",)
    save_as = save_as_new = save_on_top = True
    search_fields = (
        "enum_symbol", "func_name", "skill_name", "wearoff_msg", "chant_text",
        "appearance", "decide_func"
    )
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False
