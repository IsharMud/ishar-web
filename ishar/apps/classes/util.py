from ishar.apps.classes.models import Class


def get_classes(playable=True) -> list:
    """
    Get classes (only playable, by default).
    """
    out = []
    query = Class.objects
    if playable:
        query = query.exclude(class_description__isnull=True)
    for _class in query.all().order_by("class_id"):
        out.append((_class.class_id, _class.get_class_name()))
    return out


def get_class_options(*args, **kwargs) -> list:
    """
    Get playable classes, and append a "-1" option for NoneType.
    """
    ret = get_classes(playable=True)
    ret.append((-1, None))
    return ret
