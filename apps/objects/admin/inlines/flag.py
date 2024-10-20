from .base import ObjectBaseInline

from ...models.flag import ObjectFlag


class ObjectFlagInline(ObjectBaseInline):
    """Object flag inline administration."""

    model = ObjectFlag
    verbose_name = "Flag"
    verbose_name_plural = "Flags"
