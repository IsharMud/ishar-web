from django.db import models


class ProfessionRecipe(models.Model):
    """Game-owned profession recipe (name lookup only).

    The minimal mapping the quest catalog needs to resolve RECIPE_REWARD
    names; if a full professions app ever lands, this moves there.
    """

    id = models.AutoField(
        primary_key=True,
        help_text="Recipe ID.",
        verbose_name="Recipe ID",
    )
    name = models.CharField(
        max_length=80,
        help_text="Recipe name.",
        verbose_name="Name",
    )

    class Meta:
        managed = False
        db_table = "profession_recipes"
        verbose_name = "Profession Recipe"

    def __str__(self) -> str:
        return self.name
