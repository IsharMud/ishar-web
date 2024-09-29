from .object import Object, ObjectManager


class RelicManager(ObjectManager):
    """Filter for objects with relic flag."""
    def get_queryset(self):
        return super().get_queryset().filter(flag__relic=True)


class Relic(Object):
    """Ishar Relic (proxy model of Object, excludes regular objects)."""
    objects = RelicManager()

    class Meta:
        proxy = True
