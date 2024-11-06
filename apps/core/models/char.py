from django.db.models import CharField as DBCharField
from django.forms import CharField as FormCharField


class NoStripCharField(DBCharField):
    """Text input model field, without strip, to preserve spaces."""

    def formfield(self, **kwargs):
        # Update widget, and strip boolean, for the form field.
        defaults = {
            "widget": FormCharField,
            "strip": False
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
