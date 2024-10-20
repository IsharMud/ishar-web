from django.contrib.admin import display, ModelAdmin


class MUDClientAdmin(ModelAdmin):
    """MUD client administration."""

    fields = (
        "name",
        "category",
        "url",
        "is_visible"
    )
    list_display = (
        "name",
        "get_category_link",
        "is_visible"
    )
    list_filter = (
        "category",
        "is_visible"
    )
    list_select_related = ("category",)
    readonly_fields = ("client_id",)
    search_fields = (
        "category",
        "name",
        "url"
    )

    @display(description="Category", ordering="category")
    def get_category_link(self, obj=None) -> str:
        if obj and obj.category:
            return obj.category.get_admin_link()
        return ""

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
