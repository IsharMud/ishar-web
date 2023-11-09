# Generated by Django 4.2.7 on 2023-11-09 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_mudclientcategory_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mudclient',
            options={'default_related_name': 'mud_clients', 'managed': True, 'ordering': ('category__display_order', 'name'), 'verbose_name': 'MUD Client', 'verbose_name_plural': 'MUD Clients'},
        ),
        migrations.RemoveField(
            model_name='mudclient',
            name='display_order',
        ),
    ]
