from .object import Object, ObjectManager


class ArtifactManager(ObjectManager):
    """Filter for objects with artifact flag."""
    def get_queryset(self):
        return super().get_queryset().filter(flag__artifact=True)


class Artifact(Object):
    """Ishar Artifact (proxy model of Object, excludes regular objects)."""
    objects = ArtifactManager()

    class Meta:
        proxy = True
