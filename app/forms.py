from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms_validators import Alpha

# Log In form class
class LoginForm(FlaskForm):
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
    remember    = BooleanField('Remember Me')
    submit      = SubmitField('Log In')


# Change Password form class
class ChangePasswordForm(FlaskForm):
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
                                validators.EqualTo('new_password', message='Please make sure that your new passwords match!')
                                ]
                            )
    submit                  = SubmitField('Change Password')


# New Account form class
class NewAccountForm(FlaskForm):
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
                                validators.EqualTo('password', message='Please make sure that your passwords match!')
                                ]
                            )
    submit              = SubmitField('Create Account')


# News add form class to post news updates
class NewsAddForm(FlaskForm):
    subject     = StringField('Subject', [
                                validators.DataRequired(),
                                validators.Length(min=1, max=64),
                                ]
                            )
    body        = TextAreaField('Message', [validators.DataRequired()] )
    submit      = SubmitField('Post')


# Player search form class to search player names
class PlayerSearchForm(FlaskForm):
    player_search_name  = StringField('Player Name', [
                                    validators.DataRequired(),
                                    validators.Length(min=3, max=25),
                                    Alpha(message='Player names may only contain letters!')
                                ]
                            )
    submit              = SubmitField('Search')
