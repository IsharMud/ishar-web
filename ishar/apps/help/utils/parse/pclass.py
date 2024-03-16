from ishar.apps.classes.models import Class


def parse_help_class(class_line=None):
    """
    Parse a single class line from a single topic chunk
        from the MUD 'helptab' file, and link the Player Class help page.
    """

    topic_classes = class_line.split('/')
    num_topic_classes = len(topic_classes)
    string_out = str()
    i = 0

    playable_classes = Class.objects.filter(
        is_playable=True
    ).values_list("class_name", flat=True)

    for topic_class in topic_classes:
        i += 1
        topic_class = topic_class.strip()
        if topic_class in playable_classes:
            string_out += (
                f'<a href="/help/{topic_class}"'
                f' title="Help: {topic_class} (Class)">'
                f'{topic_class}</a>'
            )
            if i != num_topic_classes:
                string_out += ', '
        else:
            string_out = class_line
    return string_out
