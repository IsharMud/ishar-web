from .object import Object, ObjectManager


class ArtifactManager(ObjectManager):
    def get_queryset(self):
        # Filter for objects with artifact flag.
        return super().get_queryset().filter(flag__artifact=True)


class Artifact(Object):
    """Ishar Artifact (proxy model of Object, excludes regular objects)."""

    objects = ArtifactManager()

    class Meta:
        proxy = True
