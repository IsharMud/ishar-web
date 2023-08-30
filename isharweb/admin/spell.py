from django.contrib.admin import ModelAdmin, TabularInline

from ..models.spell import SpellFlag, SpellForce, Spell, SpellSpellFlag


# TODO
#   - Figure out how to get the "Add Another ..." link at the bottom
#       of the inlined Spell Flags and Spell Forces tabular forms.
#   - I can "Add another Quest Step" or "Add another Quest Reward", but
#       but they have a different type of relationship.


class SpellsFlagsAdminInline(TabularInline):
    """
    Ishar spell's flags inline administration.
    """
    extra = 1
    fieldsets = ((None, {"fields": ("spell", "flag",)}),)
    filter_horizontal = filter_vertical = list_filter = readonly_fields = ()
    list_display = search_fields = ("spell", "flag")
    model = SpellSpellFlag


class SpellsForcesAdminInline(TabularInline):
    """
    Ishar spell's forces inline administration.
    """
    extra = 1
    fieldsets = ((None, {"fields": ("spell", "force",)}),)
    filter_horizontal = filter_vertical = list_filter = readonly_fields = ()
    list_display = search_fields = ("spell", "force")
    model = SpellForce


class SpellFlagAdmin(ModelAdmin):
    """
    Ishar spell flag administration.
    """
    fieldsets = ((None, {"fields": ("id", "name", "description")}),)
    filter_horizontal = filter_vertical = list_filter = readonly_fields = ()
    inlines = (SpellsFlagsAdminInline,)
    list_display = search_fields = ("name", "description")
    model = SpellFlag


class SpellAdmin(ModelAdmin):
    """
    Ishar spell administration.
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
    filter_horizontal = filter_vertical = readonly_fields = ()
    inlines = (SpellsFlagsAdminInline, SpellsForcesAdminInline)
    list_display = ("skill_name", "_is_spell", "_is_skill", "_is_type")
    list_filter = ("is_spell", "is_skill", "is_type")
    model = Spell
    search_fields = (
        "enum_symbol", "func_name", "skill_name",
        "wearoff_msg", "chant_text", "appearance", "decide_func"
    )
