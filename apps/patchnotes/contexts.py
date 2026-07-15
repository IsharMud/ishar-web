"""Context processor: unread patch-note count for the nav/portal pill."""
from django.db import DatabaseError

from .services import unread_count


def patch_notes_unread(request):
    """
    `PATCH_NOTES_UNREAD`: how many published notes the logged-in account has not
    read. Zero for anonymous users, and defensively zero if the game tables
    aren't present yet (web deployed before the game migration).
    """
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"PATCH_NOTES_UNREAD": 0}
    try:
        return {"PATCH_NOTES_UNREAD": unread_count(user.account_id)}
    except DatabaseError:
        return {"PATCH_NOTES_UNREAD": 0}
