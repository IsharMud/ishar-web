from django.contrib.admin import StackedInline

from ishar.apps.players.models.common import PlayerCommon


class PlayerCommonInlineAdmin(StackedInline):
    """
    Player common inline administration.
    """
    model = PlayerCommon
    classes = ("collapse",)
    verbose_name = verbose_name_plural = "Common"

    def has_add_permission(self, request, obj=None) -> bool:
        """Disable adding rows to player_common."""
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disable deleting rows from player_common."""
        return False
