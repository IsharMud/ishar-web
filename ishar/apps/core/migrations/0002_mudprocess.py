# Generated by Django 5.0.2 on 2024-03-06 00:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MUDProcess',
            fields=[
                ('process_id', models.PositiveIntegerField(db_column='process_id', help_text='MUD process ID (PID) on the server.', primary_key=True, serialize=False, verbose_name='MUD Process ID (PID)')),
                ('name', models.CharField(db_column='name', default='ishar-mud', help_text='Name of the MUD process.', max_length=32, verbose_name='Name')),
                ('user', models.CharField(db_column='user', default='ishar-mud', help_text='Name of the MUD process.', max_length=32, verbose_name='Name')),
                ('last_updated', models.DateTimeField(db_column='last_updated', default=django.utils.timezone.now, help_text='Last updated date and time of the MUD process in the database.', verbose_name='Last Updated')),
            ],
            options={
                'verbose_name': 'MUD Process',
                'verbose_name_plural': 'MUD Processes',
                'db_table': 'mud_processes',
                'managed': True,
                'default_related_name': 'process',
            },
        ),
    ]