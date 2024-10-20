from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class ChallengeCompletedListFilter(admin.SimpleListFilter):
    """Admin list filter to identify (in)complete challenges."""

    title = "Completed?"
    parameter_name = "completed"

    def lookups(self, request, model_admin):
        return (
            ("1", "Yes"),
            ("0", "No")
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "1":
                queryset = queryset.exclude(winner_desc__exact="")
            if self.value() == "0":
                queryset = queryset.filter(winner_desc__exact="")
        return queryset


class ChallengeAdmin(admin.ModelAdmin):
    """Ishar challenge administration."""

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "challenge_id",
                    "is_active",
                    "is_completed"
                )
            }
        ),
        (
            "Details",
            {
                "fields": (
                    "challenge_desc",
                    "winner_desc",
                    "last_completion"
                )
            }
        ),
        (
            "Target",
            {
                "fields": ("mobile",)
            }
        ),
        (
            "Maximums",
            {
                "fields": (
                    "max_level",
                    "max_people",
                )
            },
        ),
        (
            "Totals",
            {
                "fields": (
                    "num_completed",
                    "num_picked",
                )
            },
        ),
    )
    list_display = (
        "challenge_desc",
        "mobile_link",
        "is_active",
        "is_completed"
    )
    list_filter = (
        "is_active",
        ChallengeCompletedListFilter,
        "mobile__level",
        "max_level",
        "max_people",
        "num_completed",
        "num_picked",
    )
    readonly_fields = (
        "challenge_id",
        "is_completed",
        "last_completion"
    )
    search_fields = (
        "challenge_desc",
        "winner_desc",
        "mobile__long_name",
        "mobile__name",
        "mobile__id",
    )
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    @admin.display(description="Mobile", ordering="mobile__long_name")
    def mobile_link(self, obj):
        # Admin link for mobile.
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                viewname="admin:mobiles_mobile_change",
                args=(obj.mobile.pk,)
            ),
            obj.mobile
        )
