from django.contrib.admin import site

from ..models.category import NoteCategory
from ..models.note import Note

from .category import NoteCategoryAdmin
from .note import NoteAdmin


site.register(NoteCategory, NoteCategoryAdmin)
site.register(Note, NoteAdmin)
