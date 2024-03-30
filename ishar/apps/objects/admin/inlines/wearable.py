from .base import ObjectBaseInline

from ...models.wearable import ObjectWearableFlag


class ObjectWearableFlagInline(ObjectBaseInline):
    """Object wearable flag inline administration."""
    model = ObjectWearableFlag
    verbose_name = "Wearable Flag"
    verbose_name_plural = "Wearable Flags"
