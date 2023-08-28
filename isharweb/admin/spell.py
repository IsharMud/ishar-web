from django.contrib.admin import ModelAdmin

from ..models.spell import SpellFlag, SpellForce, SpellInfo, SpellSpellFlag


class SpellInfoAdmin(ModelAdmin):
    """
    Ishar spell info administration.
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
    filter_horizontal = ()
    filter_vertical = ()
    inlines = ()
    list_display = ("skill_name", "_is_spell", "_is_skill", "_is_type")
    list_filter = ("is_spell", "is_skill", "is_type", "skill_name")
    search_fields = (
        "enum_symbol", "func_name", "skill_name",
        "wearoff_msg", "chant_text", "appearance", "decide_func"
    )
    readonly_fields = ()
