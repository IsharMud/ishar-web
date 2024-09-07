from apps.classes.models.type import PlayerClass


PLAYER_CLASS_NAMES = PlayerClass._member_map_.keys()


def parse_player_class(pcls: str) -> (list, str):
    """Parse text right of colon for a line starting with "Class"."""
    parsed = []
    pcls_line = pcls.strip()

    if pcls_line.upper() in PLAYER_CLASS_NAMES:
        parsed.append(pcls_line)

    else:
        for splitter in (",", "|", "/"):
            if splitter in pcls_line:
                for pcls_item in pcls_line.split(splitter):
                    pcls_item = pcls_item.strip()
                    if pcls_item.upper() in PLAYER_CLASS_NAMES:
                        parsed.append(pcls_item)

    if not parsed:
        parsed = pcls_line

    return parsed
