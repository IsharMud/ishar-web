PLAYER_CLASS_NAMES = (
    "Warrior", "Necromancer", "Mage", "Magician", "Shaman", "Cleric", "Rogue",
)

def parse_player_class(pcls: str) -> list:
    """Parse text right of colon for a line starting with "Class"."""
    pcls_line_value = pcls.strip()
    player_classes = []
    if pcls_line_value in PLAYER_CLASS_NAMES:
        player_classes.append(pcls_line_value)
    else:
        for splitter in (",", "|", "/"):
            if splitter in pcls_line_value:
                for pcls_item in pcls_line_value.split(splitter):
                    pcls_item = pcls_item.strip()
                    if pcls_item in PLAYER_CLASS_NAMES:
                        player_classes.append(pcls_item)
    return player_classes
