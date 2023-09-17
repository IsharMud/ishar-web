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
        return request.user.is_immortal()


class SkillsSpellFlagsAdminInline(admin.TabularInline):
    """
    Ishar skill/spell's flags inline administration.
    """
    extra = 1
    model = SkillSpellFlag

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()


class SkillsForcesAdminInline(admin.TabularInline):
    """
    Ishar skill's forces inline administration.
    """
    extra = 1
    model = SkillForce

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Ishar skill administration.
    """
    fieldsets = (
        (None, {"fields": ("enum_symbol", "func_name", "skill_name")}),
        ("Minimums", {"fields": ("min_posn", "min_use")}),
        ("Cost", {"fields": ("spell_breakpoint", "held_cost")}),
        ("Text", {
            "fields": ("wearoff_msg", "chant_text", "appearance", "decide_func")
        }),
        ("Values", {"fields": ("difficulty", "rate", "notice_chance")}),
        ("Component", {"fields": ("component_type", "component_value")}),
        ("Scale/Mod", {"fields": ("scale", "mod_stat_1", "mod_stat_2")}),
        ("Booleans", {"fields": ("is_spell", "is_skill", "is_type")})
    )
    inlines = (SkillsSpellFlagsAdminInline, SkillsForcesAdminInline)
    list_display = ("skill_name", "is_spell", "is_skill", "is_type")
    list_filter = ("is_spell", "is_skill", "is_type")
    model = Skill
    search_fields = (
        "enum_symbol", "func_name", "skill_name",
        "wearoff_msg", "chant_text", "appearance", "decide_func"
    )

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()


@admin.register(SpellFlag)
class SpellFlagAdmin(admin.ModelAdmin):
    """
    Ishar spell flag administration.
    """
    fieldsets = ((None, {"fields": ("name", "description")}),)
    list_display = search_fields = ("name", "description")
    model = SpellFlag

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()
