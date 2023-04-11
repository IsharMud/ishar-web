"""Database classes/models"""
from datetime import datetime
from functools import cached_property

from flask_login import UserMixin
from passlib.hash import md5_crypt

from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT
from sqlalchemy.orm import relationship

from delta import stringify
from database import Base, db_session

from models.player import Player


class Account(Base, UserMixin):
    """Account used to log in to the website and MUD in-game"""
    __tablename__ = 'accounts'

    account_id = Column(INTEGER(11), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    seasonal_points = Column(MEDIUMINT(4), nullable=False, server_default=text("0"))
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(36), nullable=False)
    create_isp = Column(String(25), nullable=False)
    last_isp = Column(String(25), nullable=False)
    create_ident = Column(String(25), nullable=False)
    last_ident = Column(String(25), nullable=False)
    create_haddr = Column(INTEGER(11), nullable=False)
    last_haddr = Column(INTEGER(11), nullable=False)
    account_name = Column(String(25), nullable=False, unique=True)
    account_gift = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))

    players = relationship("Player", back_populates="account")

    def change_password(self, new_password=None):
        """Method to change an account password"""
        self.password = md5_crypt.hash(new_password)
        if db_session.commit():
            return True
        return False

    def check_password(self, password=None):
        """Method to check an account password"""
        return md5_crypt.verify(password, self.password)

    @cached_property
    def display_name(self):
        """Format the account name to display"""
        return self.account_name.replace('"', '').replace("'", '').title()

    def get_id(self):
        """Flask-login account ID"""
        return self.email

    @property
    def is_active(self):
        """Boolean whether user is active"""
        return isinstance(self.account_id, int)

    @property
    def is_authenticated(self):
        """Boolean whether user is authenticated"""
        return isinstance(self.account_id, int)

    @cached_property
    def is_god(self):
        """Boolean whether user is a God"""
        for player in self.players:
            if player.is_god:
                return True
        return False

    @cached_property
    def is_artisan(self):
        """Boolean whether user is an Artisan (or above)"""
        for player in self.players:
            if player.is_artisan:
                return True
        return False

    @cached_property
    def is_consort(self):
        """Boolean whether user is a Consort (or above)"""
        for player in self.players:
            if player.is_consort:
                return True
        return False

    @cached_property
    def is_eternal(self):
        """Boolean whether user is an Eternal (or above)"""
        for player in self.players:
            if player.is_eternal:
                return True
        return False

    @cached_property
    def is_forger(self):
        """Boolean whether user is a Forger (or above)"""
        for player in self.players:
            if player.is_forger:
                return True
        return False

    @cached_property
    def is_immortal(self):
        """Boolean whether user is immortal (or above, but not consort)"""
        for player in self.players:
            if player.is_immortal:
                return True
        return False

    @cached_property
    def created(self):
        """Timedelta since account created"""
        return datetime.utcnow() - self.created_at

    @cached_property
    def created_ago(self):
        """Stringified approximate timedelta since account created"""
        return stringify(self.created) + ' ago'

    @property
    def seasonal_earned(self):
        """Amount of essence earned for the account"""
        # Start at zero (0), and return the points from
        #   the player within the account that has the highest amount
        earned = 0
        for player in self.players:
            if player.seasonal_earned > earned:
                earned = player.seasonal_earned
        return earned

    def __repr__(self):
        return (f'<Account> "{self.account_name}" ({self.account_id})')
