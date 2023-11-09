from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe


class MUDClientCategory(models.Model):
    """
    MUD Client Category.
    """
    category_id = models.AutoField(
        blank=False,
        db_column="category_id",
        help_text="Auto-generated ID number of the MUD client category.",
        null=False,
        primary_key=True,
        verbose_name="MUD Client Category ID"
    )
    name = models.CharField(
        max_length=64,
        blank=False,
        db_column="name",
        help_text="Name of the MUD client category.",
        null=False,
        verbose_name="Category Name"
    )
    is_visible = models.BooleanField(
        blank=False,
        db_column="is_visible",
        default=True,
        help_text="Should the MUD client category be visible publicly?",
        null=False,
        verbose_name="Visible?"
    )
    display_order = models.PositiveIntegerField(
        db_column="display_order",
        null=False,
        blank=False,
        unique=True,
        help_text=(
            "What is the numeric display order of the MUD client category?"
        ),
        verbose_name="Display Order"
    )

    class Meta:
        managed = True
        db_table = "mud_client_categories"
        default_related_name = "mud_client_categories"
        ordering = ("display_order",)
        verbose_name = "MUD Client Category"
        verbose_name_plural = "MUD Client Categories"

    def get_absolute_url(self) -> str:
        return reverse(viewname="clients") + "#category-" + self.category_id

    def get_admin_link(self) -> str:
        return mark_safe(
            '<a href="%s" title="%s">%s</a>' % (
                self.get_admin_url(),
                self.name,
                self.name
            )
        )

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:clients_mudclientcategory_change",
            args=(self.category_id,)
        )

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.name


class MUDClient(models.Model):
    """
    MUD Client.
    """
    client_id = models.AutoField(
        blank=False,
        help_text="Auto-generated ID number of the MUD client.",
        null=False,
        primary_key=True,
        verbose_name="MUD Client ID"
    )
    category = models.ForeignKey(
        db_column="category_id",
        blank=False,
        help_text="Category of the MUD client.",
        null=False,
        on_delete=models.PROTECT,
        related_query_name="client",
        related_name="clients",
        to=MUDClientCategory,
        verbose_name="Category",
    )
    name = models.CharField(
        max_length=64,
        blank=False,
        db_column="name",
        help_text="Name of the MUD client.",
        null=False,
        unique=True,
        verbose_name="Name"
    )
    url = models.URLField(
        blank=False,
        db_column="url",
        help_text="URL of the MUD client.",
        null=False,
        verbose_name="URL"
    )
    is_visible = models.BooleanField(
        blank=False,
        db_column="is_visible",
        default=True,
        help_text="Should the MUD client be visible publicly?",
        null=False,
        verbose_name="Visible?"
    )

    class Meta:
        managed = True
        db_table = "mud_clients"
        default_related_name = "mud_clients"
        ordering = ("category__display_order", "name")
        verbose_name = "MUD Client"
        verbose_name_plural = "MUD Clients"

    def get_absolute_url(self) -> str:
        return reverse(viewname="clients") + "#client-" + self.client_id

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:clients_mudclient_change",
            args=(self.client_id,)
        )

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.name
