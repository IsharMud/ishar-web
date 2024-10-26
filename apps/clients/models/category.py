from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class MUDClientCategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key of the MUD client category name.
        return self.get(name=name)


class MUDClientCategory(models.Model):
    """Website MUD client category."""

    objects = MUDClientCategoryManager()

    category_id = models.AutoField(
        blank=False,
        db_column="category_id",
        help_text="Auto-generated ID number of the MUD client category.",
        null=False,
        primary_key=True,
        verbose_name="MUD Client Category ID",
    )
    name = models.CharField(
        max_length=64,
        blank=False,
        db_column="name",
        help_text="Name of the MUD client category.",
        null=False,
        verbose_name="Category Name",
    )
    is_visible = models.BooleanField(
        blank=False,
        db_column="is_visible",
        default=True,
        help_text="Should the MUD client category be visible publicly?",
        null=False,
        verbose_name="Visible?",
    )
    display_order = models.PositiveIntegerField(
        db_column="display_order",
        null=False,
        blank=False,
        unique=True,
        help_text=(
            "What is the numeric display order of the MUD client category?"
        ),
        verbose_name="(Display) Order"
    )
    display_icon = models.CharField(
        max_length=64,
        blank=True,
        db_column="display_icon",
        help_text="Bootstrap icon to display with the MUD client category.",
        null=True,
        verbose_name="(Display) Icon",
    )

    class Meta:
        managed = True
        db_table = "mud_client_categories"
        default_related_name = "mud_client_categories"
        ordering = ("display_order",)
        verbose_name = "MUD Client Category"
        verbose_name_plural = "MUD Client Categories"

    def get_absolute_url(self) -> str:
        return f'{reverse(viewname="clients")}#category-{self.category_id}'

    def get_admin_link(self) -> str:
        return format_html(
            '<a href="{}" title="{}">{}</a>',
            self.get_admin_url(), self.name, self.name
        )

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:clients_mudclientcategory_change",
            args=(self.category_id,)
        )

    def get_display_icon(self) -> str:
        if self.display_icon:
            return format_html(
                '<i class="bi bi-{}"></i>',
                self.display_icon
            )
        return ''

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name

    def natural_key(self) -> str:
        # Natural key of the MUD client category name.
        return self.name
