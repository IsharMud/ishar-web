from django.contrib import admin

from apps.news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Ishar news administration.
    """
    date_hierarchy = "created"
    fieldsets = (
        (None, {"fields": ("news_id",)}),
        ("Content", {"fields": ("subject", "body")}),
        ("Authorship", {"fields": ("created", "account")}),
    )
    list_display = ("subject", "created", "is_visible", "account")
    list_filter = ("is_visible", ("account", admin.RelatedOnlyFieldListFilter),)
    readonly_fields = ("news_id", "account")
    search_fields = ("subject", "body", "account", "is_visible")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.account = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
            if obj and obj.account and request.user == obj.account:
                return True
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
            if obj and obj.account and request.user == obj.account:
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
