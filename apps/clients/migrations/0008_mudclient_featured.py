from django.db import migrations, models


def feature_mudlet(apps, schema_editor):
    # Mudlet ships an official Ishar package, so it gets the featured card.
    MUDClient = apps.get_model("clients", "MUDClient")
    MUDClient.objects.filter(name__iexact="mudlet").update(
        is_featured=True,
        featured_note=(
            "Officially supported — install the Ishar package from "
            "Mudlet's package repository."
        ),
    )


def unfeature_mudlet(apps, schema_editor):
    MUDClient = apps.get_model("clients", "MUDClient")
    MUDClient.objects.filter(name__iexact="mudlet").update(
        is_featured=False,
        featured_note="",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0007_mudclientcategory_display_icon"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mudclient",
            options={
                "default_related_name": "mud_clients",
                "managed": True,
                "ordering": (
                    "category__display_order", "-is_featured", "name",
                ),
                "verbose_name": "MUD Client",
                "verbose_name_plural": "MUD Clients",
            },
        ),
        migrations.AddField(
            model_name="mudclient",
            name="is_featured",
            field=models.BooleanField(
                db_column="is_featured",
                default=False,
                help_text=(
                    "Is the MUD client specially supported by Ishar "
                    "(featured card, listed first in its category)?"
                ),
                verbose_name="Featured?",
            ),
        ),
        migrations.AddField(
            model_name="mudclient",
            name="featured_note",
            field=models.CharField(
                blank=True,
                db_column="featured_note",
                default="",
                help_text=(
                    "Short note shown on the featured card, e.g. where to "
                    "find the official Ishar package."
                ),
                max_length=128,
                verbose_name="Featured Note",
            ),
        ),
        migrations.RunPython(feature_mudlet, unfeature_mudlet),
    ]
