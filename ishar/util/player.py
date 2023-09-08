from ishar.apps.players.models import PlayerClass


def get_classes(playable=True):
    """
    Get classes (only playable, by default).
    """
    out = []
    query = PlayerClass.objects
    if playable:
        query = query.exclude(class_description__isnull=True)
    for _class in query.all():
        out.append((_class.class_id, _class.class_name.title()))
    return out


def get_class_options(*args, **kwargs):
    ret = get_classes()
    ret.append((-1, "None"))
    return ret
