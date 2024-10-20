from django.db import models
from django.utils.translation import gettext_lazy as _

from .mobile import Mobile


class MobileDescription(models.Model):
    """Mobile description."""

    id = models.AutoField(
        db_column="id",
        primary_key=True,
        help_text=_(
            "Auto-generated, permanent ID number of the mobile description."
        ),
        verbose_name=_("Mobile Description ID")
    )
    mobile = models.ForeignKey(
        db_column="mob_id",
        to=Mobile,
        to_field="id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text="Mobile with an extra description.",
        verbose_name="Mobile",
    )
    extra_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Extra name of the mobile.",
        verbose_name="Extra Name",
    )
    extra_description = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="Extra description of the mobile.",
        verbose_name="Extra Description",
    )

    class Meta:
        managed = False
        db_table = "mob_extra_descriptions"
        ordering = ("-id",)
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("mobile", "extra_name"),
                name="one_extra_name_per_mobile"
            ),
        )
        unique_together = (("mobile", "extra_name"),)
        verbose_name = "Description"
        verbose_name_plural = "Descriptions"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.extra_name
