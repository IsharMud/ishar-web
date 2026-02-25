# from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

import settings
from .category import NoteCategory


class NoteManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key of the note name.
        return self.get(name=name)


class Note(models.Model):
    """Website admin note."""

    objects = NoteManager()

    note_id = models.AutoField(
        blank=False,
        help_text="Auto-generated ID number of the note.",
        null=False,
        primary_key=True,
        verbose_name="Note ID",
    )
    category = models.ForeignKey(
        db_column="category_id",
        blank=True,
        help_text="Category of the note.",
        null=True,
        on_delete=models.PROTECT,
        related_query_name="note",
        related_name="notes",
        to=NoteCategory,
        verbose_name="Category",
    )
    name = models.CharField(
        max_length=64,
        blank=False,
        db_column="name",
        help_text="Name of the note.",
        null=False,
        unique=True,
        verbose_name="Name",
    )
    body = models.TextField(
        blank=True,
        db_column="body",
        help_text="Body of the note.",
        null=True,
        verbose_name="Note",
    )
    note_file = models.FileField(
        max_length=100,
        help_text="PDF file related the note.",
        verbose_name="Note File",
        upload_to=settings.NOTES_URL,
        blank=True,
        null=True,
        # validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    class Meta:
        managed = True
        db_table = "notes"
        default_related_name = "notes"
        ordering = ("name",)
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def get_absolute_url(self) -> str:
        return f'{reverse(viewname="notes")}#note-{self.note_id}'

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:notes_note_change",
            args=(self.note_id,)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name

    def natural_key(self) -> str:
        # Natural key of the note name.
        return self.name
