"""Flask forms classes"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, EmailField, IntegerField, \
    PasswordField, StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms_validators import Alpha


class ChangePasswordForm(FlaskForm):
    """Change Password form class"""
    current_password        = PasswordField('Current Password',
                                validators  = [
                                    DataRequired(),
                                    Length(min=4, max=36)
                                ]
                            )
    new_password            = PasswordField('New Password',
                                validators  = [
                                    DataRequired(),
                                    Length(min=4, max=36)
                                ]
                            )
    confirm_new_password    = PasswordField('Confirm New Password',
                                validators  = [
                                    DataRequired(),
                                    Length(min=4, max=36),
                                    EqualTo('new_password',
                                        message = 'Please make sure that the passwords match!'
                                    )
                                ]
                            )
    submit                  = SubmitField('Change Password')


class EditAccountForm(FlaskForm):
    """Edit Account form class"""
    account_name        = StringField('Friendly Name',
                            validators  = [
                                DataRequired(),
                                Length(min=3, max=25),
                                Alpha(message='Please only use letters in the friendly name!')
                            ]
                        )
    email               = EmailField('E-mail Address',
                            validators  = [
                                DataRequired(),
                                Email()
                            ]
                        )
    seasonal_points     = IntegerField('Seasonal Points')
    password            = PasswordField('Password')
    confirm_password    = PasswordField('Confirm Password',
                            validators  = [
                                EqualTo('password',
                                    message = 'Please make sure that the passwords match!'
                                )
                            ]
                        )
    submit              = SubmitField('Edit Account')


class EditPlayerForm(FlaskForm):
    """Edit Player form class"""
    name        = StringField('Player Name',
                    validators  = [
                        DataRequired(),
                        Length(min=3, max=32),
                        Alpha(message='Please only use letters in the player name!')
                    ]
                )
    title       = StringField('Title', validators=[DataRequired(), Length(min=2, max=32)])
    money       = IntegerField('Karma', validators=[DataRequired()])
    align       = IntegerField('Align', validators=[DataRequired()])
    karma       = IntegerField('Karma', validators=[DataRequired()])
    sex         = IntegerField('Sex (Gender)', validators=[DataRequired()])
    renown      = IntegerField('Renown', validators=[DataRequired()])
    is_deleted  = BooleanField('Is Deleted?', validators=[DataRequired()])
    submit      = SubmitField('Edit Player')


class LoginForm(FlaskForm):
    """Log In form class"""
    email       = EmailField('E-mail Address', validators= [DataRequired(), Email()])
    password    = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=36)])
    remember    = BooleanField('Remember Me?')
    submit      = SubmitField('Log In')


class NewsAddForm(FlaskForm):
    """News add form class, for Gods to post news updates"""
    subject     = StringField('Subject', validators=[DataRequired(), Length(min=1,max=64)])
    body        = TextAreaField('Message', validators=[DataRequired()])
    submit      = SubmitField('Post')


class PlayerSearchForm(FlaskForm):
    """Player search form class to search player names"""
    player_search_name  = StringField('Player Name',
                            validators  = [
                                DataRequired(),
                                Length(min=3, max=25),
                                Alpha(message='Player names may only contain letters!')
                            ]
                        )
    submit              = SubmitField('Search')


class SeasonCycleForm(FlaskForm):
    """Season Cycle form class"""
    effective_date  = DateTimeLocalField('Effective Date',
                        format      = '%Y-%m-%dT%H:%M',
                        default     = datetime.utcnow(),
                        validators  = [DataRequired()]
                    )
    expiration_date = DateTimeLocalField('Expiration Date',
                        format      = '%Y-%m-%dT%H:%M',
                        default     = datetime.now() + relativedelta(months=+4),
                        validators  = [DataRequired()]
                    )
    confirm_wipe    = BooleanField('Are you sure you want to DELETE all mortal players?',
                        validators  = [DataRequired()]
                    )
    submit          = SubmitField('Cycle Seasons')

class QuestEditorForm(FlaskForm):
    """Quest Editor form class"""
    name = StringField('Name', validators=[DataRequired(), Length(max=25)])
    display_name = StringField('Display Name', validators=[DataRequired(), Length(max=30)])
    min_level = IntegerField('Minimum Level', validators=[DataRequired(), NumberRange(min=1, max=20)])
    repeatable = BooleanField('Repeatable', default=False)
    description = StringField('Description', validators=[DataRequired(), Length(max=512)])
    class_restrict = IntegerField('Class Restriction', validators=[DataRequired(), NumberRange(min=0, max=9)])
    quest_intro = StringField('Quest Introduction', validators=[DataRequired(), Length(max=1600)])
    prerequisites = SelectMultipleField('Quest Prerequisites', choices=[], coerce=int)

class QuestStepEditorForm(FlaskForm):
    """Quest Step form class"""
    step_type = SelectField('Step Type', choices=[(0, 'Object'), (1, 'Kill'), (2, 'Room')], validators=[DataRequired()])
    target = IntegerField('Target', validators=[DataRequired()])
    num_required = IntegerField('Number Required', validators=[DataRequired()])
    time_limit = IntegerField('Time Limit')
    mystify = BooleanField('Mystify', default=False)
    mystify_text = StringField('Mystify Text', validators=[DataRequired()])

class QuestRewardEditorForm(FlaskForm):
    """Quest Reward form class"""
    reward_num = IntegerField('Reward Number', validators=[DataRequired()])
    reward_type = SelectField('Reward Type', choices=[
        (0, 'Object_always'),
        (1, 'Object_Choice'),
        (2, 'Money'),
        (3, 'Alignment'),
        (4, 'Skill'),
        (5, 'Renown'),
        (6, 'Experience'),
        (7, 'Quest')
    ], validators=[DataRequired()])