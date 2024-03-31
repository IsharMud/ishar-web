from django.contrib import admin

from ..models.skill import Skill

from .inlines.component import SkillComponentAdminInline
from .inlines.mod import SkillModAdminInline
from .inlines.skill_force import SkillForceAdminInline
from .inlines.spell_flag import SkillSpellFlagAdminInline


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Skill administration.
    """
    fieldsets = (
        (None, {"fields": ("id", "enum_symbol", "func_name", "skill_name")}),
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
        ("Type", {"fields": ("skill_type",)}),
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
        "skill_type", "min_posn",
        ("flag", admin.EmptyFieldListFilter),
        ("mod", admin.RelatedOnlyFieldListFilter)
    )
    model = Skill
    ordering = ("-skill_type", "skill_name")
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
            return request.user.is_god()
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False
