from django.contrib.admin import ModelAdmin


class ClassAdmin(ModelAdmin):
    """
    Ishar class administration.
    """
    fieldsets = (
        (None, {"fields": (
            "class_id", "class_name", "class_display", "class_description"
        )}),
    )
    filter_horizontal = []
    filter_vertical = []
    list_display = ("class_name", "class_display", "class_description")
    list_filter = []
    readonly_fields = ["class_id"]
    search_fields = ["class_name", "class_display", "class_description"]


class PlayerAdmin(ModelAdmin):
    """
    Ishar player administration.
    """

    def has_add_permission(self, request, obj=None):
        """
        Remove ability to add players in /admin/.
        """
        return False

    fieldsets = (
        (None, {"fields": (
            "id", "account", "name", "description", "true_level", "online"
        )}),
        ("Survival", {"fields":("game_type", "is_deleted")}),
        ("Points", {"fields": ("bankacc", "renown", "remorts", "favors")}),
        ("Totals", {"fields": (
            "deaths", "total_renown", "quests_completed", "challenges_completed"
        )}),
        ("Rooms", {"fields": ["bound_room", "load_room", "inn_limit"]}),
        ("Dates", {"fields": ["birth", "logon", "logout"]})
    )
    filter_horizontal = []
    filter_vertical = []
    list_display = [
        "name", "account", "player_type", "level", "renown",
        "_is_deleted", "_is_god", "_is_immortal", "_is_survival"
    ]
    list_filter = ["game_type", "is_deleted", "true_level", "account"]
    readonly_fields = ["id", "account", "birth", "logon", "logout"]
    search_fields = ["name"]
