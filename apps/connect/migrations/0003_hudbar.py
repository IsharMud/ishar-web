import apps.core.models.unsigned
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("connect", "0002_questtrack"),
    ]

    operations = [
        migrations.CreateModel(
            name="HudBar",
            fields=[
                (
                    "id",
                    apps.core.models.unsigned.UnsignedAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                (
                    "player_id",
                    models.IntegerField(
                        help_text="players.id of the character the bar belongs to.",
                        unique=True,
                        verbose_name="Player ID",
                    ),
                ),
                (
                    "account_id",
                    models.IntegerField(
                        db_index=True,
                        help_text="Owning account id (denormalized for ownership scoping).",
                        verbose_name="Account ID",
                    ),
                ),
                (
                    "slots",
                    models.JSONField(
                        default=list,
                        help_text=(
                            "Ordered action-bar slots: skill keys (strings), "
                            "pinned-item objects, or null for an empty slot. "
                            "Sanitized server-side."
                        ),
                        verbose_name="Slots",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="When the bar was last saved.",
                        verbose_name="Updated At",
                    ),
                ),
            ],
            options={
                "verbose_name": "HUD Bar",
                "verbose_name_plural": "HUD Bars",
                "db_table": "web_hud_bar",
                "managed": True,
            },
        ),
    ]
