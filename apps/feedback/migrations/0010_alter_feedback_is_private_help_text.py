from django.db import migrations, models


class Migration(migrations.Migration):
    """Private reports are now promotable to the private GitHub tracker; refresh
    the ``is_private`` help text to match. The ``feedback`` table is owned by the
    game (``managed = False``), so this only updates Django's model state and the
    admin display — no DDL runs against the database."""

    dependencies = [
        ("feedback", "0009_feedback_feedbackcomment_feedbacksynctask_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="is_private",
            field=models.BooleanField(
                db_column="is_private",
                default=False,
                help_text=(
                    "Private reports never reach Discord (likely-exploit "
                    "reports). They can still be promoted to the private GitHub "
                    "tracker, where issues stay admin-only."
                ),
                verbose_name="Private?",
            ),
        ),
    ]
