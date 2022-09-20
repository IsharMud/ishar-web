"""
Flask forms classes
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, EmailField, PasswordField, \
    RadioField, StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms_validators import Alpha


class LoginForm(FlaskForm):
    """
    Log In form class
    """
    email       = EmailField('E-mail Address', [
                    validators.DataRequired(),
                    validators.Email()
                    ]
                )
    password    = PasswordField('Password', [
                    validators.DataRequired(),
                    validators.Length(min=4, max=36)
                    ]
                )
    remember    = BooleanField('Remember Me?')
    submit      = SubmitField('Log In')


class SeasonAddForm(FlaskForm):
    """
    Season Add form class
    """
    effective_date  = DateTimeLocalField('Effective Date',
                        format      = '%Y-%m-%dT%H:%M',
                        default     = datetime.utcnow(),
                        validators  = [validators.DataRequired()]
                    )
    expiration_date = DateTimeLocalField('Expiration Date',
                        format      = '%Y-%m-%dT%H:%M',
                        default     = datetime.now() + relativedelta(months=+4),
                        validators  = [validators.DataRequired()]
                    )
    expire_active   = BooleanField('Expire Active?', default=True)
    submit          = SubmitField('Add Season')


class ShopForm(FlaskForm):
    """
    Shop form class
    """
    upgrade     = RadioField('Upgrade', coerce=int)
    submit      = SubmitField('Purchase')


class ChangePasswordForm(FlaskForm):
    """
    Change Password form class
    """
    current_password        = PasswordField('Current Password', [
                                validators.DataRequired(),
                                validators.Length(min=4, max=36)
                                ]
                            )
    new_password            = PasswordField('New Password', [
                                validators.DataRequired(),
                                validators.Length(min=4, max=36)
                                ]
                            )
    confirm_new_password    = PasswordField('Confirm New Password', [
                                validators.DataRequired(),
                                validators.Length(min=4, max=36),
                                validators.EqualTo('new_password',
                                    message='Please make sure that your new passwords match!')
                                ]
                            )
    submit                  = SubmitField('Change Password')


class NewAccountForm(FlaskForm):
    """
    New Account form class
    """
    account_name        = StringField('Friendly Name', [
                                validators.DataRequired(),
                                validators.Length(min=3, max=25),
                                Alpha(message='Please only use letters in your friendly name!')
                                ]
                            )
    email               = EmailField('E-mail Address', [
                                validators.DataRequired(),
                                validators.Email()
                                ]
                            )
    password            = PasswordField('Password', [
                                validators.DataRequired(),
                                validators.Length(min=4, max=36)
                                ]
                            )
    confirm_password    = PasswordField('Confirm Password', [
                                validators.DataRequired(),
                                validators.Length(min=4, max=36),
                                validators.EqualTo('password',
                                    message='Please make sure that your passwords match!')
                                ]
                            )
    submit              = SubmitField('Create Account')


class NewsAddForm(FlaskForm):
    """
    News add form class, for Gods to post news updates
    """
    subject     = StringField('Subject', [
                                validators.DataRequired(),
                                validators.Length(min=1, max=64),
                                ]
                            )
    body        = TextAreaField('Message', [validators.DataRequired()])
    submit      = SubmitField('Post')


class PlayerSearchForm(FlaskForm):
    """
    Player search form class to search player names
    """
    player_search_name  = StringField('Player Name', [
                                    validators.DataRequired(),
                                    validators.Length(min=3, max=25),
                                    Alpha(message='Player names may only contain letters!')
                                ]
                            )
    submit              = SubmitField('Search')
