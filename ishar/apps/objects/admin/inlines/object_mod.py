from .base import ObjectBaseInline

from ...models.object_mod import ObjectObjectMod


class ObjectModInline(ObjectBaseInline):
    """Object mod inline administration."""
    model = ObjectObjectMod
