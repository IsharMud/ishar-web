from django.contrib import admin

from ..models.classes import Class


class PlayableClassListFilter(admin.SimpleListFilter):
    title = "Playable?"
    parameter_name = "is_playable"

    def lookups(self, request, model_admin):
        return (
            (1, "Yes"),
            (0, "No")
        )

    def queryset(self, request, queryset):
        """
        Determine whether a class is playable based on whether
            the "class_description" column is NULL.
        """
        qs = queryset
        if self.value():
            if self.value() == "1":
                qs = qs.exclude(class_description=None)
            if self.value() == "0":
                qs = qs.filter(class_description=None)
        return qs


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """
    Ishar class administration.
    """
    fieldsets = (
        (None, {"fields": ("class_id", "class_name", "is_playable")}),
        ("Details", {"fields": ("class_display", "class_description")})
    )
    list_filter = (PlayableClassListFilter,)
    readonly_fields = ("class_id", "is_playable")
    list_display = (
        "class_name", "is_playable", "class_display", "class_description"
    )
    search_fields = ("class_name", "class_display", "class_description")

    def has_add_permission(self, request, obj=None):
        return request.user.is_god()

    def has_change_permission(self, request, obj=None):
        return request.user.is_god()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_god()

