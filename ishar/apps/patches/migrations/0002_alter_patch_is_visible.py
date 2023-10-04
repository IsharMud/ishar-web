# Generated by Django 4.2.4 on 2023-09-20 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patches', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patch',
            name='is_visible',
            field=models.BooleanField(default=True, help_text='Should the patch be visible publicly?', verbose_name='Visible?'),
        ),
    ]
