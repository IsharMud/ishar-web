from django.contrib.admin import ModelAdmin


class NewsAdmin(ModelAdmin):
    """
    Ishar news administration.
    """
    fieldsets = (
        (None, {"fields": ("news_id",)}),
        ("Content", {"fields": ("subject", "body", "created_at", "account")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("subject", "created_at", "account")
    list_filter = ("account",)
    readonly_fields = ("news_id",)
    search_fields = ("subject", "body")
