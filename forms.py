"""Flask forms classes"""
from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, DateTimeLocalField, EmailField, \
    IntegerField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, \
    NumberRange
from wtforms_validators import Alpha, AlphaSpace

from mud_secret import ALIGNMENTS


class ChangePasswordForm(FlaskForm):
    """Change Password form class"""
    current_password = PasswordField(
        'Current Password',
        validators=[
            DataRequired(),
            Length(min=4, max=36)
        ]
    )
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=4, max=36)
        ]
    )
    confirm_new_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            Length(min=4, max=36),
            EqualTo(
                'new_password',
                message='Please make sure that the passwords match!'
            )
        ]
    )
    submit = SubmitField('Change Password')


class EditAccountForm(FlaskForm):
    """Edit Account form class"""
    account_name = StringField(
        'Friendly Name',
        validators=[
            DataRequired(),
            Length(min=3, max=25),
            Alpha(
                message='Please only use letters in the friendly name!'
            )
        ]
    )
    email = EmailField(
        'E-mail Address',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    seasonal_points = IntegerField('Seasonal Points')
    password = PasswordField('Password')
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            EqualTo(
                'password',
                message='Please make sure that the passwords match!'
            )
        ]
    )
    submit = SubmitField('Edit Account')


class EditPlayerForm(FlaskForm):
    """Edit Player form class"""
    name = StringField(
        'Player Name',
        validators=[
            DataRequired(),
            Length(min=3, max=32),
            Alpha(
                message='Please only use letters in the player name!'
            )
        ]
    )
    alignment = IntegerField(
        'Alignment',
        validators=[
            NumberRange(
                min=min(min(ALIGNMENTS.values())),
                max=max(max(ALIGNMENTS.values()))
            )
        ]
    )
    gold = IntegerField(
        'Gold',
        validators=[
            NumberRange(min=0, max=100000)
        ]
    )
    karma = IntegerField(
        'Karma',
        validators=[
            NumberRange(min=-100000, max=100000)
        ]
    )
    renown = IntegerField(
        'Renown',
        validators=[
            NumberRange(min=0)
        ]
    )
    is_deleted = BooleanField('Is Deleted?')
    submit = SubmitField('Edit Player')


class EventAddForm(FlaskForm):
    """Event Add form class"""
    event_type = IntegerField(
        'Type',
        validators=[
            NumberRange(min=0)
        ]
    )
    start_time = DateTimeLocalField(
        'Start',
        default=datetime.utcnow(),
    )
    end_time = DateTimeLocalField(
        'End',
        default=datetime.utcnow() + relativedelta(days=+1),
    )
    event_name = StringField(
        'Name',
        validators=[
            DataRequired(),
        ]
    )
    event_desc = StringField(
        'Description'
    )
    xp_bonus = IntegerField(
        'XP Bonus',
        validators=[
            NumberRange(min=0)
        ]
    )
    shop_bonus = IntegerField(
        'Shop Bonus',
        validators=[
            NumberRange(min=0)
        ]
    )
    celestial_luck = IntegerField(
        'Celestial Luck',
        validators=[
            NumberRange(min=0)
        ]
    )
    submit = SubmitField('Save')


class HelpSearchForm(FlaskForm):
    """Help search form class to search help topic names"""
    search = StringField(
        'Topic',
        validators=[
            DataRequired(),
            Length(min=2, max=32),
            AlphaSpace(
                message='Topic names may only contain between 2-32 letters!'
            )
        ]
    )
    submit = SubmitField('Search')


class LoginForm(FlaskForm):
    """Log In form class"""
    email = EmailField(
        'E-mail Address',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4, max=36)
        ]
    )
    remember = BooleanField('Remember Me?')
    submit = SubmitField('Log In')


class NewsAddForm(FlaskForm):
    """News add form class, for Gods to post news updates"""
    subject = StringField(
        'Subject',
        validators=[
            DataRequired(),
            Length(min=1, max=64)
        ]
    )
    body = TextAreaField(
        'Message',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Post')


class PlayerSearchForm(FlaskForm):
    """Player search form class to search player names"""
    player_search_name = StringField(
        'Player Name',
        validators=[
            DataRequired(),
            Length(min=3, max=25),
            Alpha(
                message='Player names may only contain letters!'
            )
        ]
    )
    submit = SubmitField('Search')


class PatchAddForm(FlaskForm):
    """Patch Add form class"""
    name = StringField(
        'Name',
        default='Patch_X.Y',
        validators=[
            DataRequired(),
            Length(min=5, max=32),
        ]
    )
    file = FileField(
        'File',
        validators=[
            FileRequired()
        ]
    )
    submit = SubmitField('Upload')


class SeasonCycleForm(FlaskForm):
    """Season Cycle form class"""
    effective_date = DateTimeLocalField(
        'Effective Date',
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow(),
        validators=[
            DataRequired()
        ]
    )
    expiration_date = DateTimeLocalField(
        'Expiration Date',
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow() + relativedelta(months=+4),
        validators=[
            DataRequired()
        ]
    )
    confirm_wipe = BooleanField(
        'Are you sure you want to DELETE all mortal players?',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Cycle Seasons')
