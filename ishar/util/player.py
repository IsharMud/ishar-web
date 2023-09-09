from django.conf import settings

from ishar.apps.players.models import Class


def get_classes(playable=True):
    """
    Get classes (only playable, by default).
    """
    out = []
    query = Class.objects
    if playable:
        query = query.exclude(class_description__isnull=True)
    for _class in query.all():
        out.append((_class.class_id, _class.class_name.title()))
    return out


def get_class_options(*args, **kwargs):
    """
    Get playable classes, and append a "-1" option for "None".
    """
    ret = get_classes(playable=True)
    ret.append((-1, "None"))
    return ret
