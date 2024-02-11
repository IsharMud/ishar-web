from copy import copy

from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import mark_safe

from ishar.apps.skills.models.skill import Skill

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
    list_filter = ("skill_type", "min_posn")
    model = Skill
    ordering = ("-skill_type", "skill_name")
    readonly_fields = ("id",)
    # actions = ("duplicate",)
    save_as = True
    save_as_continue = True
    save_on_top = True
    search_fields = (
        "enum_symbol", "func_name", "skill_name",
        "wearoff_msg", "chant_text", "appearance", "decide_func"
    )

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

    def duplicate(self, request, queryset):
        for obj in queryset:
            duped_obj = copy(obj)
            duped_obj.skill_name += " Copy"
            duped_obj.pk = None
            try:
                duped_obj.save()
                if duped_obj.pk:

                    for flag in obj.flags.all():
                        duped_obj.flags.add(flag)
                    for force in obj.forces.all():
                        duped_obj.forces.add(force)
                    for component in obj.components.all():
                        duped_obj.components.add(component)

                    duped_obj.save()

                    messages.success(
                        request,
                        message=mark_safe(
                            "Record duplicated as %s." % (
                                '<a href="%s">%s<a/>' % (
                                    reverse(
                                        viewname="admin:skills_skill_change",
                                        args=(duped_obj.pk,)
                                    ),
                                    duped_obj
                                )
                            )
                        )
                    )

            except Exception as dupe_exc:
                print(dupe_exc)
                messages.error(
                    request,
                    message=(
                        "There was an error trying to duplicate the record(s)."
                    )
                )

    duplicate.short_description = "Duplicate selected record"
