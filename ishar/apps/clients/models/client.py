from django.db import models
from django.urls import reverse

from .category import MUDClientCategory


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
        return "%s#client-%i" % (reverse(viewname="clients"), self.client_id)

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:clients_mudclient_change",
            args=(self.client_id,)
        )

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return self.name
