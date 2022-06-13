from app import app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import hmac
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, SmallInteger, String, Table
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
db = SQLAlchemy(app)

# Account database class
class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    seasonal_points = Column(Integer, nullable=False, server_default=FetchedValue())
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(36), nullable=False)
    create_isp = Column(String(25), nullable=False)
    last_isp = Column(String(25), nullable=False)
    create_ident = Column(String(25), nullable=False)
    last_ident = Column(String(25), nullable=False)
    create_haddr = Column(Integer, nullable=False)
    last_haddr = Column(Integer, nullable=False)
    account_name = Column(String(25), nullable=False, unique=True)
    players = relationship('Player', lazy='select', backref='account')

    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)

    def get_id(self):
        return str(self.account_id)

    def is_authenticated(self):
        return isinstance(self.account_id, int)

    def is_active(self):
        return isinstance(self.account_id, int)

    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)


# Player database class
class Player(db.Model):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    create_ident = Column(String(10), nullable=False, server_default=FetchedValue())
    last_isp = Column(String(30), nullable=False, server_default=FetchedValue())
    description = Column(String(240))
    title = Column(String(45), nullable=False, server_default=FetchedValue())
    poofin = Column(String(80), nullable=False, server_default=FetchedValue())
    poofout = Column(String(80), nullable=False, server_default=FetchedValue())
    bankacc = Column(Integer, nullable=False)
    logon_delay = Column(SmallInteger, nullable=False)
    true_level = Column(Integer, nullable=False)
    renown = Column(Integer, nullable=False)
    prompt = Column(String(42), nullable=False, server_default=FetchedValue())
    remorts = Column(Integer, nullable=False)
    favors = Column(Integer, nullable=False)
    birth = Column(Integer, nullable=False)
    logon = Column(Integer, nullable=False)
    online = Column(Integer)
    logout = Column(Integer, nullable=False)
    bound_room = Column(Integer, nullable=False)
    load_room = Column(Integer, nullable=False)
    wimpy = Column(SmallInteger)
    invstart_level = Column(Integer)
    color_scheme = Column(SmallInteger)
    sex = Column(Integer, nullable=False)
    race_id = Column(ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    class_id = Column(ForeignKey('classes.class_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    level = Column(Integer, nullable=False)
    weight = Column(SmallInteger, nullable=False)
    height = Column(SmallInteger, nullable=False)
    align = Column(SmallInteger, nullable=False)
    comm = Column(SmallInteger, nullable=False)
    karma = Column(SmallInteger, nullable=False)
    experience_points = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    fg_color = Column(SmallInteger, nullable=False)
    bg_color = Column(SmallInteger, nullable=False)
    login_failures = Column(SmallInteger, nullable=False)
    create_haddr = Column(Integer, nullable=False)
    auto_level = Column(Integer, nullable=False)
    login_fail_haddr = Column(Integer)
    last_haddr = Column(Integer)
    last_ident = Column(String(10), server_default=FetchedValue())
    load_room_next = Column(Integer)
    load_room_next_expires = Column(Integer)
    aggro_until = Column(Integer)
    inn_limit = Column(SmallInteger, nullable=False)
    held_xp = Column(Integer)
    last_isp_change = Column(Integer)
    perm_hit_pts = Column(Integer, nullable=False)
    perm_move_pts = Column(Integer, nullable=False)
    perm_spell_pts = Column(Integer, nullable=False)
    perm_favor_pts = Column(Integer, nullable=False)
    curr_hit_pts = Column(Integer, nullable=False)
    curr_move_pts = Column(Integer, nullable=False)
    curr_spell_pts = Column(Integer, nullable=False)
    curr_favor_pts = Column(Integer, nullable=False)
    init_strength = Column(Integer, nullable=False)
    init_agility = Column(Integer, nullable=False)
    init_endurance = Column(Integer, nullable=False)
    init_perception = Column(Integer, nullable=False)
    init_focus = Column(Integer, nullable=False)
    init_willpower = Column(Integer, nullable=False)
    curr_strength = Column(Integer, nullable=False)
    curr_agility = Column(Integer, nullable=False)
    curr_endurance = Column(Integer, nullable=False)
    curr_perception = Column(Integer, nullable=False)
    curr_focus = Column(Integer, nullable=False)
    curr_willpower = Column(Integer, nullable=False)
    is_deleted = Column(Integer, nullable=False, server_default=FetchedValue())
    deaths = Column(Integer, nullable=False, server_default=FetchedValue())
    total_renown = Column(Integer, nullable=False, server_default=FetchedValue())
    quests_completed = Column(Integer, nullable=False, server_default=FetchedValue())
    challenges_completed = Column(Integer, nullable=False, server_default=FetchedValue())
