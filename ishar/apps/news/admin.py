from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Ishar news administration.
    """
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("news_id",)}),
        ("Content", {"fields": ("subject", "body")}),
        ("Authorship", {"fields": ("created_at", "account")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("subject", "created_at", "account")
    list_filter = (("account", admin.RelatedOnlyFieldListFilter),)
    readonly_fields = ("news_id", "account")
    search_fields = ("subject", "body", "account")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.account = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return request.user.is_god()

    def has_change_permission(self, request, obj=None):
        if request.user.is_god():
            return True
        if obj and obj.account and request.user == obj.account:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_god():
            return True
        if obj and obj.account and request.user == obj.account:
            return True
        return False

    def has_module_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()
