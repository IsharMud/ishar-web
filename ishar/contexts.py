from ishar.apps.season.models import Season


def current_season(request):
    """
    Current Ishar MUD season context processor for Django templates.
    """
    return {"current_season": Season.objects.filter(is_active=1).first()}
