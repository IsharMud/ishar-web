# Generated by Django 5.0.3 on 2024-03-06 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_mudprocess_options_mudprocess_created_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MUDProcess',
        ),
    ]