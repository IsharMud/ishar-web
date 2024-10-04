from .object import Object, ObjectManager


class RelicManager(ObjectManager):
    def get_queryset(self):
        # Filter for objects with relic flag.
        return super().get_queryset().filter(flag__relic=True)


class Relic(Object):
    """Ishar Relic (proxy model of Object, excludes regular objects)."""
    objects = RelicManager()

    class Meta:
        proxy = True
