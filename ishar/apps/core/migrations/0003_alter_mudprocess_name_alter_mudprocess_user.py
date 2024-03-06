# Generated by Django 5.0.2 on 2024-03-06 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_mudprocess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mudprocess',
            name='name',
            field=models.CharField(db_column='name', default='ishar', help_text='Name of the MUD process.', max_length=32, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='mudprocess',
            name='user',
            field=models.CharField(db_column='user', help_text='Name of the MUD process.', max_length=32, verbose_name='Name'),
        ),
    ]
