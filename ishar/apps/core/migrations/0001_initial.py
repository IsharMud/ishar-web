# Generated by Django 5.0.2 on 2024-03-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AffectFlag',
            fields=[
                ('flag_id', models.PositiveIntegerField(help_text='Auto-generated identification number of the affect flag.', primary_key=True, serialize=False, verbose_name='Affect Flag ID')),
                ('name', models.CharField(help_text='(Internal) name of the affect flag.', max_length=30, unique=True, verbose_name='Name')),
                ('display_name', models.CharField(help_text='Display name of the affect flag.', max_length=100, verbose_name='Display Name')),
                ('is_beneficial', models.IntegerField(blank=True, help_text='Is the affect flag beneficial?', null=True, verbose_name='Beneficial?')),
                ('item_description', models.CharField(help_text='Item description of the affect flag.', max_length=100, verbose_name='Item Description')),
            ],
            options={
                'verbose_name': 'Affect Flag',
                'verbose_name_plural': 'Affect Flags',
                'db_table': 'affect_flags',
                'ordering': ('display_name',),
                'managed': False,
                'default_related_name': 'affect_flag',
            },
        ),
        migrations.CreateModel(
            name='PlayerFlag',
            fields=[
                ('flag_id', models.PositiveIntegerField(db_column='flag_id', help_text='Auto-generated identification number of the player flag.', primary_key=True, serialize=False, verbose_name='Player Flag ID')),
                ('name', models.CharField(db_column='name', help_text='Name of the player flag.', max_length=20, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Player/Mobile Flag',
                'db_table': 'player_flags',
                'ordering': ('name', 'flag_id'),
                'managed': False,
            },
        ),
    ]