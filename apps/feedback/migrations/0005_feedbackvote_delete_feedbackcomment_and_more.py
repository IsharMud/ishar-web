# Generated by Django 5.0.8 on 2024-10-06 17:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_feedbacksubmission_private_feedbackcomment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackVote',
            fields=[
                ('vote_id', models.AutoField(db_column='vote_id', help_text='Auto-generated permanent ID number of the feedback vote.', primary_key=True, serialize=False, verbose_name='Vote ID')),
                ('vote_value', models.BooleanField(db_column='vote_value', help_text='Positive (True) or negative (False) boolean value of the vote.', verbose_name='Value')),
                ('voted', models.DateTimeField(auto_now_add=True, db_column='voted', help_text='Date and time of the vote.', verbose_name='Voted')),
                ('account', models.ForeignKey(db_column='account_id', help_text='Account that voted on the feedback submission.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Account')),
                ('feedback_submission', models.ForeignKey(db_column='submission_id', help_text='Feedback submission that was voted on.', on_delete=django.db.models.deletion.CASCADE, to='feedback.feedbacksubmission', verbose_name='Feedback Submission')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
                'db_table': 'feedback_votes',
                'ordering': ('-voted',),
                'get_latest_by': ('voted',),
                'managed': True,
                'default_related_name': 'votes',
            },
        ),
        migrations.DeleteModel(
            name='FeedbackComment',
        ),
        migrations.AddConstraint(
            model_name='feedbackvote',
            constraint=models.UniqueConstraint(fields=('account', 'feedback_submission'), name='one_vote_per'),
        ),
        migrations.AlterUniqueTogether(
            name='feedbackvote',
            unique_together={('account', 'feedback_submission')},
        ),
    ]
