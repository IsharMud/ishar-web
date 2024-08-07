from django.db import models
from django import forms

class TextareaField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super().formfield(**defaults)
