# Generated by Django 4.2.7 on 2023-11-19 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_mudclient_name_alter_mudclientcategory_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mudclient',
            name='client_id',
            field=models.AutoField(help_text='Auto-generated ID number of the MUD client.', primary_key=True, serialize=False, verbose_name='MUD Client ID'),
        ),
    ]
