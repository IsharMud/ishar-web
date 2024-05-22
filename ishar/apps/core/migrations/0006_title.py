# Generated by Django 5.0.3 on 2024-03-09 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_delete_mudprocess'),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('title_id', models.AutoField(help_text='Primary key identification number of the title.', primary_key=True, serialize=False, verbose_name='Title ID')),
                ('male_text', models.CharField(blank=True, help_text='Male text of the title.', max_length=100, null=True, verbose_name='Male Text')),
                ('female_text', models.CharField(blank=True, help_text='Female text of the title.', max_length=100, null=True, verbose_name='Female Text')),
                ('prepend', models.BooleanField(blank=True, help_text='Should the title be prepended?', null=True, verbose_name='Prepend?')),
            ],
            options={
                'verbose_name': 'Title',
                'verbose_name_plural': 'Titles',
                'db_table': 'titles',
                'ordering': ('title_id',),
                'managed': False,
            },
        ),
    ]
