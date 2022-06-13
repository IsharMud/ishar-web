# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, SmallInteger, String, Table
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class AccountUpgrade(Base):
    __tablename__ = 'account_upgrades'

    id = Column(Integer, primary_key=True)
    cost = Column(Integer, nullable=False)
    description = Column(String(200), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    max_value = Column(Integer, nullable=False, server_default=FetchedValue())



class Account(Base):
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



t_accounts_account_upgrades = Table(
    'accounts_account_upgrades', metadata,
    Column('account_upgrades_id', ForeignKey('account_upgrades.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('account_id', ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('amount', Integer, nullable=False)
)



class AffectFlag(Base):
    __tablename__ = 'affect_flags'

    flag_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)



class Board(Base):
    __tablename__ = 'boards'

    board_id = Column(Integer, primary_key=True)
    board_name = Column(String(15), nullable=False)



class Class(Base):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True)
    class_name = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())



class Condition(Base):
    __tablename__ = 'conditions'

    condition_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)



class DisplayOption(Base):
    __tablename__ = 'display_options'

    display_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)



t_player_affect_flags = Table(
    'player_affect_flags', metadata,
    Column('affect_flag_id', ForeignKey('affect_flags.flag_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('expires', Integer, nullable=False),
    Column('flag_value', Integer, nullable=False),
    Column('bits', Integer, nullable=False),
    Column('location_1', Integer, nullable=False),
    Column('mod_1', Integer, nullable=False),
    Column('location_2', Integer, nullable=False),
    Column('mod_2', Integer, nullable=False),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
)



t_player_boards = Table(
    'player_boards', metadata,
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('board_id', ForeignKey('boards.board_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('last_read', Integer, nullable=False)
)



t_player_conditions = Table(
    'player_conditions', metadata,
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('condition_id', ForeignKey('conditions.condition_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', SmallInteger, nullable=False)
)



t_player_display_options = Table(
    'player_display_options', metadata,
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('display_id', ForeignKey('display_options.display_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', Integer, nullable=False)
)



class PlayerFlag(Base):
    __tablename__ = 'player_flags'

    flag_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)



t_player_player_flags = Table(
    'player_player_flags', metadata,
    Column('flag_id', ForeignKey('player_flags.flag_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', Integer, nullable=False)
)



t_player_quests = Table(
    'player_quests', metadata,
    Column('quest_id', ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', Integer, nullable=False)
)



t_player_remort_upgrades = Table(
    'player_remort_upgrades', metadata,
    Column('upgrade_id', ForeignKey('remort_upgrades.upgrade_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', Integer, nullable=False)
)



t_player_skills = Table(
    'player_skills', metadata,
    Column('skill_id', ForeignKey('skills.skill_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('skill_level', Integer, nullable=False)
)



class Player(Base):
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

    account = relationship('Account', primaryjoin='Player.account_id == Account.account_id', backref='players')
    _class = relationship('Class', primaryjoin='Player.class_id == Class.class_id', backref='players')
    race = relationship('Race', primaryjoin='Player.race_id == Race.race_id', backref='players')



class Quest(Base):
    __tablename__ = 'quests'

    quest_id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True, server_default=FetchedValue())



class Race(Base):
    __tablename__ = 'races'

    race_id = Column(Integer, primary_key=True)
    race_name = Column(String(15), nullable=False, unique=True)



class RemortUpgrade(Base):
    __tablename__ = 'remort_upgrades'

    upgrade_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True, server_default=FetchedValue())
    renown_cost = Column(SmallInteger, nullable=False)
    max_value = Column(SmallInteger, nullable=False)



class Season(Base):
    __tablename__ = 'seasons'

    season_id = Column(Integer, primary_key=True)
    is_active = Column(Integer, nullable=False)
    effective_date = Column(Integer, nullable=False)
    expiration_date = Column(Integer, nullable=False)



class Skill(Base):
    __tablename__ = 'skills'

    skill_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
