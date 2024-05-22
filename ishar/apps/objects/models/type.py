from django.db.models import IntegerChoices


class ObjectType(IntegerChoices):
    """Object type choices."""
    NO_TYPE = 0
    LIGHT = 1
    WEAPON = 2
    ARMOR = 3
    KEY = 4
    SCROLL = 5
    WAND = 6
    STAFF = 7
    POTION = 8
    CHEST = 9
    SACK = 10
    DRINK = 11
    FOOD = 12
    TRAP = 13
    TREASURE = 14
    NOTE = 15
    BOAT = 16
    OTHER = 17
    MONEY = 18
    LOOT = 19
    MARK = 20
    TOTEM = 21
    QUEST = 22
    TOME = 23
    TEMPORAL = 24
    COMPONENT = 25
    TEMPORAL_COMPONENT = 26
    MAX_OBJECT = 27

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self):
        return self.name.title()
