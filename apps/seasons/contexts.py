from .utils import get_current_season


def current_season(request):
    """Context processor for current Ishar MUD season."""
    return {"CURRENT_SEASON": get_current_season()}
