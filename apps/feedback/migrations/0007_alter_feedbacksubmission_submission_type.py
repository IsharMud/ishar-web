# Generated by Django 5.1.2 on 2024-10-11 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_remove_feedbacksubmission_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbacksubmission',
            name='submission_type',
            field=models.IntegerField(choices=[(-1, 'Complete'), (0, 'Other'), (1, 'Bug'), (2, 'Idea')], db_column='submission_type', default=0, help_text='Type of the feedback submission.', verbose_name='Type'),
        ),
    ]
