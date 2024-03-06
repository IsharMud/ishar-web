from django.db import models
from django.utils import timezone


class Achievement(models.Model):
    """Ishar achievement."""
    achievement_id = models.AutoField(
        primary_key=True,
        help_text="Primary key identification number of the achievement.",
        verbose_name="Achievement ID"
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the achievement.",
        verbose_name="Name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the achievement.",
        verbose_name="Description"
    )
    is_hidden = models.BooleanField(
        help_text="Is the achievement hidden?",
        verbose_name="Hidden?"
    )
    created_at = models.DateTimeField(
        help_text="Creation time of the achievement.",
        verbose_name="Created"
    )
    updated_at = models.DateTimeField(
        help_text="Updated time of the achievement.",
        verbose_name="Updated"
    )
    category = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Category of the achievement.",
        verbose_name="Category"
    )

    class Meta:
        managed = False
        db_table = "achievements"
        default_related_name = "achievement"
        ordering = ("-is_hidden", "name")
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Update timestamps on save."""
        now = timezone.now()
        if not self.pk:
            self.created_at = now
        self.updated_at = now
        return super().save(*args, **kwargs)
