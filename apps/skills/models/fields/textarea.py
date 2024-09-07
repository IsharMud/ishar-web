from django.db.models import TextField
from django.forms import Textarea


class NoStripTextareaField(TextField):
    """Text area model field, without strip, to preserve trailing newline."""

    def formfield(self, **kwargs):
        """Update widget and strip boolean for the form field."""
        defaults = {
            "widget": Textarea,
            "strip": False
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
