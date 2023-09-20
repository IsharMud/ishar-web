from django.contrib import admin

from .models import Force, SkillForce, Skill, SkillSpellFlag, SpellFlag


@admin.register(Force)
class ForceAdmin(admin.ModelAdmin):
    """
    Ishar force administration.
    """
    fields = ("id", "force_name")
    list_display = list_display_links = search_fields = fields
    readonly_fields = ("id",)

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


class SkillsSpellFlagsAdminInline(admin.TabularInline):
    """
    Ishar skill/spell's flags inline administration.
    """
    extra = 1
    model = SkillSpellFlag

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


class SkillsForcesAdminInline(admin.TabularInline):
    """
    Ishar skill's forces inline administration.
    """
    extra = 1
    model = SkillForce

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Ishar skill administration.
    """
    fieldsets = (
        (None, {"fields": ("id", "enum_symbol", "func_name", "skill_name")}),
        ("Minimums", {"fields": ("min_posn", "min_use")}),
        ("Cost", {"fields": ("spell_breakpoint", "held_cost")}),
        ("Text", {
            "fields": ("wearoff_msg", "chant_text", "appearance", "decide_func")
        }),
        ("Values", {"fields": ("difficulty", "rate", "notice_chance")}),
        ("Component", {"fields": ("component_type", "component_value")}),
        ("Scale/Mod", {"fields": ("scale", "mod_stat_1", "mod_stat_2")}),
        ("Booleans", {"fields": ("is_spell", "is_skill", "is_type")}),
        ("Type", {"fields": ("skill_type",)}),
        ("Parent", {"fields": ("parent_skill",)})
    )
    inlines = (SkillsSpellFlagsAdminInline, SkillsForcesAdminInline)
    list_display = (
        "skill_name", "skill_type", "is_spell", "is_skill", "is_type"
    )
    list_filter = ("skill_type", "is_spell", "is_skill", "is_type")
    model = Skill
    readonly_fields = ("id",)
    search_fields = (
        "enum_symbol", "func_name", "skill_name",
        "wearoff_msg", "chant_text", "appearance", "decide_func"
    )

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


@admin.register(SpellFlag)
class SpellFlagAdmin(admin.ModelAdmin):
    """
    Ishar spell flag administration.
    """
    fieldsets = ((None, {"fields": ("name", "description")}),)
    list_display = search_fields = ("name", "description")
    model = SpellFlag

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False
