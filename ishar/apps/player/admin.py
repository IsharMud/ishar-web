from django.contrib import admin

from .models import PlayerClass, Player


@admin.register(PlayerClass)
class PlayerClassAdmin(admin.ModelAdmin):
    """
    Ishar class administration.
    """
    fieldsets = ((None, {"fields": (
        "class_id", "class_name", "class_display", "class_description"
    )}),)
    filter_horizontal = filter_vertical = list_filter = ()
    readonly_fields = ("class_id",)
    list_display = search_fields = (
        "class_name", "class_display", "class_description"
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Ishar player administration.
    """

    def has_add_permission(self, request, obj=None):
        """
        Disable adding players in /admin/.
        """
        return False

    fieldsets = (
        (None, {"fields": (
            "id", "account", "name", "description",
            "true_level", "game_type", "is_deleted", "online"
        )}),
        ("Points", {"fields": ("bankacc", "renown", "remorts", "favors")}),
        ("Totals", {"fields": (
            "deaths", "total_renown", "quests_completed", "challenges_completed"
        )}),
        ("Rooms", {"fields": ("bound_room", "load_room", "inn_limit")}),
        ("Dates", {"fields": ("birth", "logon", "logout")})
    )
    filter_horizontal = filter_vertical = ()
    list_display = (
        "name", "account", "player_type", "level", "renown",
        "is_deleted", "is_god", "is_immortal", "is_survival"
    )
    list_filter = ("game_type", "is_deleted", "true_level", "account")
    readonly_fields = ("id", "birth", "logon", "logout")
    search_fields = ("name", "account__account_name")
