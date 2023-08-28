from django.contrib.admin import ModelAdmin


class RaceAdmin(ModelAdmin):
    """
    Ishar race administration.
    """
    fieldsets = (
        (None, {"fields": [
                    'id',
                    'account',
                    'name',
                    'description',
                    'bankacc',
                    'true_level',
                    'renown',
                    'remorts',
                    'favors',
                    'online',
                    'is_deleted',
                    'deaths',
                    'total_renown',
                    'quests_completed',
                    'challenges_completed',
                    'game_type',
                ]
            }
        ),
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
    ordering = ["id"]
    readonly_fields = ["id", "account", "birth", "logon", "logout"]
    search_fields = ["name"]
