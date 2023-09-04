"""
isharmud.com context processors for Django templates.
"""
from ishar.apps.season.models import Season


def current_season(request):
    """
    Current Ishar MUD season.
    """
    return {"current_season": Season.objects.filter(is_active=1).first()}
