from .base import ObjectBaseInline

from ...models.object_mod import ObjectObjectMod


class ObjectObjectModInline(ObjectBaseInline):
    """Object mod inline administration."""

    model = ObjectObjectMod
    verbose_name = "Mod"
    verbose_name_plural = "Mods"
