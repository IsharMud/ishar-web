from .base import ObjectBaseInline

from ...models.extra import ObjectExtra


class ObjectExtraInline(ObjectBaseInline):
    """Object extra inline administration."""
    model = ObjectExtra
    verbose_name = "Extra"
    verbose_name_plural = "Extras"
