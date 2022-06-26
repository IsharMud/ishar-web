from app import app
import crypt
import hmac
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms_validators import Alpha
from sqlalchemy import exc, Column, DateTime, ForeignKey, Integer, MetaData, SmallInteger, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

# Connect to the database
db = SQLAlchemy(app)

# Log In form class
class LoginForm(FlaskForm):
    email       = EmailField('E-mail Address', [
                    validators.DataRequired(),
                    validators.Email()
                    ]
                )
    password    = PasswordField('Password', [
                    validators.DataRequired(),
                    validators.Length(min=6, max=36)
                    ]
                )
    remember    = BooleanField('Remember Me')
    submit      = SubmitField('Log In')


# Change Password form class
class ChangePasswordForm(FlaskForm):
    current_password        = PasswordField('Current Password', [
                                validators.DataRequired(),
                                validators.Length(min=6, max=36)
                                ]
                            )
    new_password            = PasswordField('New Password', [
                                validators.DataRequired(),
                                validators.Length(min=6, max=36)
                                ]
                            )
    confirm_new_password    = PasswordField('Confirm New Password', [
                                validators.DataRequired(),
                                validators.Length(min=6, max=36),
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
                                validators.Length(min=6, max=36)
                                ]
                            )
    confirm_password    = PasswordField('Confirm Password', [
                                validators.DataRequired(),
                                validators.Length(min=6, max=36),
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


# Account database class
class Account(db.Model, UserMixin):
    __tablename__   = 'accounts'
    account_id      = Column(Integer, primary_key=True)
    created_at      = Column(DateTime, nullable=False, server_default=FetchedValue())
    seasonal_points = Column(Integer, nullable=False, server_default=FetchedValue())
    email           = Column(String(30), nullable=False, unique=True)
    password        = Column(String(36), nullable=False)
    create_isp      = Column(String(25), nullable=False)
    last_isp        = Column(String(25), nullable=False)
    create_ident    = Column(String(25), nullable=False)
    last_ident      = Column(String(25), nullable=False)
    create_haddr    = Column(Integer, nullable=False)
    last_haddr      = Column(Integer, nullable=False)
    account_name    = Column(String(25), nullable=False, unique=True)
    players         = relationship('Player',
                        lazy='select',
                        backref='account'
                    )

    def get_id(self):
        return str(self.account_id)

    def is_authenticated(self):
        return isinstance(self.account_id, int)

    def is_active(self):
        return isinstance(self.account_id, int)

    # Accounts with a player above a certain level are administrators
    def is_admin(self, admin_level):
        for player in self.players:
            if player.true_level > admin_level:
                return True

        return False

    # Method to allow users to change their account password
    def change_password(self, new_password):
        try:
            self.password = crypt.crypt(new_password, crypt.mksalt(method=crypt.METHOD_MD5))
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return e

    # Method to check an account password
    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)

    # Method to create new account
    def create_account(self):
        try:
            self.password = crypt.crypt(self.password, crypt.mksalt(method=crypt.METHOD_MD5))
            db.session.add(self)
            db.session.commit()
            return self.account_id
        except Exception as e:
            print(e)
            return e


# Player Class database class
class PlayerClass(db.Model):
    __tablename__   = 'classes'
    class_id        = Column(Integer, primary_key=True)
    class_name      = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())


# Player Flag database class
class PlayerFlag(db.Model):
    __tablename__   = 'player_flags'
    flag_id         = Column(Integer, primary_key=True)
    name            = Column(String(20), nullable=False, unique=True)


# Players Flags database class
class PlayersFlags(db.Model):
    __tablename__   = 'player_player_flags'
    flag_id         = Column(
                        ForeignKey('player_flags.flag_id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    value           = Column(Integer)
    flag_name       = relationship('PlayerFlag',
                        primaryjoin='PlayersFlags.flag_id == PlayerFlag.flag_id',
                        backref='player_flags'
                    )

# Player Race database class
class PlayerRace(db.Model):
    __tablename__   = 'races'
    race_id         = Column(Integer, primary_key=True)
    race_name       = Column(String(15), nullable=False, unique=True)

# Player database class
class Player(db.Model):
    __tablename__           = 'players'
    id                      = Column(Integer, primary_key=True)
    account_id              = Column(
                                ForeignKey('accounts.account_id',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    name                    = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    create_ident            = Column(String(10), nullable=False, server_default=FetchedValue())
    last_isp                = Column(String(30), nullable=False, server_default=FetchedValue())
    description             = Column(String(240))
    title                   = Column(String(45), nullable=False, server_default=FetchedValue())
    poofin                  = Column(String(80), nullable=False, server_default=FetchedValue())
    poofout                 = Column(String(80), nullable=False, server_default=FetchedValue())
    bankacc                 = Column(Integer, nullable=False)
    logon_delay             = Column(SmallInteger, nullable=False)
    true_level              = Column(Integer, nullable=False)
    renown                  = Column(Integer, nullable=False)
    prompt                  = Column(String(42), nullable=False, server_default=FetchedValue())
    remorts                 = Column(Integer, nullable=False)
    favors                  = Column(Integer, nullable=False)
    birth                   = Column(Integer, nullable=False)
    logon                   = Column(Integer, nullable=False)
    online                  = Column(Integer)
    logout                  = Column(Integer, nullable=False)
    bound_room              = Column(Integer, nullable=False)
    load_room               = Column(Integer, nullable=False)
    wimpy                   = Column(SmallInteger)
    invstart_level          = Column(Integer)
    color_scheme            = Column(SmallInteger)
    sex                     = Column(Integer, nullable=False)
    race_id                 = Column(
                                ForeignKey('races.race_id',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    class_id                = Column(
                                ForeignKey('classes.class_id',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    level                   = Column(Integer, nullable=False)
    weight                  = Column(SmallInteger, nullable=False)
    height                  = Column(SmallInteger, nullable=False)
    align                   = Column(SmallInteger, nullable=False)
    comm                    = Column(SmallInteger, nullable=False)
    karma                   = Column(SmallInteger, nullable=False)
    experience_points       = Column(Integer, nullable=False)
    money                   = Column(Integer, nullable=False)
    fg_color                = Column(SmallInteger, nullable=False)
    bg_color                = Column(SmallInteger, nullable=False)
    login_failures          = Column(SmallInteger, nullable=False)
    create_haddr            = Column(Integer, nullable=False)
    auto_level              = Column(Integer, nullable=False)
    login_fail_haddr        = Column(Integer)
    last_haddr              = Column(Integer)
    last_ident              = Column(String(10), server_default=FetchedValue())
    load_room_next          = Column(Integer)
    load_room_next_expires  = Column(Integer)
    aggro_until             = Column(Integer)
    inn_limit               = Column(SmallInteger, nullable=False)
    held_xp                 = Column(Integer)
    last_isp_change         = Column(Integer)
    perm_hit_pts            = Column(Integer, nullable=False)
    perm_move_pts           = Column(Integer, nullable=False)
    perm_spell_pts          = Column(Integer, nullable=False)
    perm_favor_pts          = Column(Integer, nullable=False)
    curr_hit_pts            = Column(Integer, nullable=False)
    curr_move_pts           = Column(Integer, nullable=False)
    curr_spell_pts          = Column(Integer, nullable=False)
    curr_favor_pts          = Column(Integer, nullable=False)
    init_strength           = Column(Integer, nullable=False)
    init_agility            = Column(Integer, nullable=False)
    init_endurance          = Column(Integer, nullable=False)
    init_perception         = Column(Integer, nullable=False)
    init_focus              = Column(Integer, nullable=False)
    init_willpower          = Column(Integer, nullable=False)
    curr_strength           = Column(Integer, nullable=False)
    curr_agility            = Column(Integer, nullable=False)
    curr_endurance          = Column(Integer, nullable=False)
    curr_perception         = Column(Integer, nullable=False)
    curr_focus              = Column(Integer, nullable=False)
    curr_willpower          = Column(Integer, nullable=False)
    is_deleted              = Column(Integer, nullable=False, server_default=FetchedValue())
    deaths                  = Column(Integer, nullable=False, server_default=FetchedValue())
    total_renown            = Column(Integer, nullable=False, server_default=FetchedValue())
    quests_completed        = Column(Integer, nullable=False, server_default=FetchedValue())
    challenges_completed    = Column(Integer, nullable=False, server_default=FetchedValue())
    player_class            = relationship('PlayerClass',
                                primaryjoin='Player.class_id == PlayerClass.class_id',
                                backref='players'
                            )
    player_flags            = relationship('PlayersFlags',
                                primaryjoin='Player.id == PlayersFlags.player_id',
                                backref='players'
                            )
    player_race             = relationship('PlayerRace',
                                primaryjoin='Player.race_id == PlayerRace.race_id',
                                backref='players'
                            )

# News database class
class News(db.Model):
    __tablename__   = 'news'
    news_id         = Column(Integer, primary_key=True)
    account_id      = Column(
                        ForeignKey('accounts.account_id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True
                    )
    created_at      = Column(DateTime, nullable=False, server_default=FetchedValue())
    subject         = Column(String(64), nullable=False, server_default=FetchedValue())
    body            = Column(Text, nullable=False)
    account         = relationship('Account',
                        primaryjoin='News.account_id == Account.account_id',
                        backref='news'
                    )


    # Method to create new account
    def add_news(self, subject=None, body=None):
        try:
            db.session.add(self)
            db.session.commit()
            return self.news_id
        except Exception as e:
            print(e)


# Season database class
class Season(db.Model):
    __tablename__   = 'seasons'
    season_id       = Column(Integer, primary_key=True)
    is_active       = Column(Integer, nullable=False)
    effective_date  = Column(Integer, nullable=False)
    expiration_date = Column(Integer, nullable=False)

# Challenge database class
class Challenge(db.Model):
    __tablename__   = 'challenges'
    challenge_id    = Column(SmallInteger, primary_key=True)
    mob_vnum        = Column(Integer, nullable=False)
    orig_level      = Column(Integer, nullable=False)
    orig_people     = Column(Integer, nullable=False)
    orig_tier       = Column(Integer, nullable=False)
    adj_level       = Column(Integer, nullable=False)
    adj_people      = Column(Integer, nullable=False)
    adj_tier        = Column(Integer, nullable=False)
    challenge_desc  = Column(String(80), nullable=False)
    winner_desc     = Column(String(80), nullable=False, server_default=FetchedValue())
    mob_name        = Column(String(30), nullable=False)
    is_active       = Column(Integer, nullable=False, server_default=FetchedValue())
