from .base import ObjectBaseInline

from ...models.affect_flag import ObjectAffectFlag


class ObjectAffectFlagInline(ObjectBaseInline):
    """Object affect flag inline administration."""

    model = ObjectAffectFlag
    verbose_name = "Affect Flag"
    verbose_name_plural = "Affect Flags"
