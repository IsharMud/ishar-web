from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html

from .inlines.affect_flag import MobileAffectFlagTabularInline
from .inlines.desc import MobileDescriptionTabularInline
from .inlines.flag import MobileFlagTabularInline

from ..models.mobile import Mobile


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    """Ishar mobile administration."""
    list_display = ("id", "long_name", "level", "description", "is_challenge")
    list_display_links = ("id", "long_name")
    list_filter = (
        "mob_class", "level", "race", "sex",
        ("spec_func", admin.EmptyFieldListFilter),
        ("challenge", admin.EmptyFieldListFilter),
    )
    readonly_fields = ("id",)
    search_fields = (
        "id", "name", "long_name", "room_desc", "description", "spec_func"
    )
    inlines = (
        MobileDescriptionTabularInline,
        MobileAffectFlagTabularInline,
        MobileFlagTabularInline,
    )
    show_full_result_count = True
    show_facets = admin.ShowFacets.ALWAYS

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    @admin.display(
        boolean=True, description="Challenge?", ordering="challenge"
    )
    def is_challenge(self, obj=None) -> bool:
        return obj.is_challenge()

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        if obj.is_challenge():
            messages.info(
                request=request,
                message=format_html(
                    'This mobile is a <a href="{}">challenge</a>.',
                    reverse(
                        viewname="admin:challenges_challenge_change",
                        args=(obj.challenge.first().pk,)
                    )
                )
            )
        return super().render_change_form(
            request, context, add, change, form_url, obj
        )
