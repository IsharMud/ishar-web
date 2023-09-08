from django.contrib import admin

from .models import Force, SpellFlag, SpellForce, Spell, SpellSpellFlag


@admin.register(Force)
class ForceAdmin(admin.ModelAdmin):
    """
    Ishar force administration.
    """
    fieldsets = ((None, {"fields": ("force_name",)}),)
    filter_horizontal = filter_vertical = list_filter = readonly_fields = ()
    list_display = search_fields = ("force_name",)

    def has_add_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_change_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()



class SpellsFlagsAdminInline(admin.StackedInline):
    """
    Ishar spell's flags inline administration.
    """
    extra = 1
    model = SpellSpellFlag

    def has_add_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_change_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()


class SpellsForcesAdminInline(admin.StackedInline):
    """
    Ishar spell's forces inline administration.
    """
    extra = 1
    model = SpellForce

    def has_add_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_change_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()


@admin.register(SpellFlag)
class SpellFlagAdmin(admin.ModelAdmin):
    """
    Ishar spell flag administration.
    """
    fieldsets = ((None, {"fields": ("name", "description")}),)
    filter_horizontal = filter_vertical = list_filter = ()
    list_display = search_fields = ("name", "description")
    model = SpellFlag

    def has_add_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_change_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()


@admin.register(SpellSpellFlag)
class SpellsFlagsAdmin(admin.ModelAdmin):
    """
    Ishar spell flag administration.
    """
    fieldsets = ((None, {"fields": ("id", "spell", "flag")}),)
    list_display = search_fields = ("id", "spell", "flag")
    list_filter = ("flag",)
    readonly_fields = ("id",)
    model = SpellSpellFlag

    def has_add_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_change_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
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
    list_display = ("skill_name", "is_spell", "is_skill", "is_type")
    list_filter = ("is_spell", "is_skill", "is_type")
    model = Spell
    search_fields = (
        "enum_symbol", "func_name", "skill_name",
        "wearoff_msg", "chant_text", "appearance", "decide_func"
    )

    def has_add_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_change_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()
