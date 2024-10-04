from django.contrib import admin

from .object import ObjectAdmin


class RelicAdmin(ObjectAdmin):
    """Ishar relic administration."""

    list_filter = (
        "deleted", "item_type",
        ("enchant", admin.RelatedOnlyFieldListFilter),
        ("grant_skill", admin.RelatedOnlyFieldListFilter),
        ("appearance", admin.EmptyFieldListFilter),
        ("description", admin.EmptyFieldListFilter),
        ("func", admin.EmptyFieldListFilter),
        ("extra", admin.EmptyFieldListFilter),
        "created_at", "updated_at"
    )
