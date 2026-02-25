from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class NoteCategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key of the note category name.
        return self.get(name=name)


class NoteCategory(models.Model):
    """Website admin note category."""

    objects = NoteCategoryManager()

    category_id = models.AutoField(
        blank=False,
        db_column="category_id",
        help_text="Auto-generated ID number of the note category.",
        null=False,
        primary_key=True,
        verbose_name="Note Category ID",
    )
    category_name = models.CharField(
        max_length=64,
        blank=False,
        db_column="name",
        help_text="Name of the note category.",
        null=False,
        verbose_name="Category Name",
    )

    class Meta:
        managed = True
        db_table = "note_categories"
        default_related_name = "note_categories"
        ordering = ("category_name",)
        verbose_name = "Note Category"
        verbose_name_plural = "Notes Categories"

    def get_absolute_url(self) -> str:
        return f'{reverse(viewname="notes")}#category-{self.category_id}'

    def get_admin_link(self) -> str:
        return format_html(
            '<a href="{}" title="{}">{}</a>',
            self.get_admin_url(), self.category_name, self.category_name
        )

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:notes_notecategory_change",
            args=(self.category_id,)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.category_name

    def natural_key(self) -> str:
        # Natural key of the note category name.
        return self.category_name
