# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AccountUpgrade(Base):
    __tablename__ = 'account_upgrades'

    id = Column(TINYINT(4), primary_key=True)
    cost = Column(MEDIUMINT(4), nullable=False)
    description = Column(String(200), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    max_value = Column(MEDIUMINT(4), nullable=False, server_default=text("1"))
    scale = Column(TINYINT(4), nullable=False, server_default=text("1"))
    is_disabled = Column(TINYINT(1), nullable=False, server_default=text("0"))


class Account(Base):
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

    players = relationship('Player', secondary='player_accounts', use_list=False)


class Challenge(Base):
    __tablename__ = 'challenges'

    challenge_id = Column(SMALLINT(4), primary_key=True)
    mob_vnum = Column(INTEGER(11), nullable=False)
    orig_level = Column(TINYINT(4), nullable=False)
    orig_people = Column(TINYINT(4), nullable=False)
    orig_tier = Column(TINYINT(4), nullable=False)
    adj_level = Column(TINYINT(4), nullable=False)
    adj_people = Column(TINYINT(4), nullable=False)
    adj_tier = Column(TINYINT(4), nullable=False)
    challenge_desc = Column(String(80), nullable=False)
    winner_desc = Column(String(80), nullable=False, server_default=text("'--'"))
    mob_name = Column(String(30), nullable=False)
    is_active = Column(TINYINT(1), nullable=False, server_default=text("0"))


class Class(Base):
    __tablename__ = 'classes'

    class_id = Column(TINYINT(3), primary_key=True)
    class_name = Column(String(15), nullable=False, unique=True, server_default=text("'NO_CLASS'"))
    class_display = Column(String(32))
    class_description = Column(String(64))



class PlayerFlag(Base):
    __tablename__ = 'player_flags'

    flag_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)


class Quest(Base):
    __tablename__ = 'quests'

    quest_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False, unique=True, server_default=text("''"))
    display_name = Column(String(30), nullable=False)
    is_major = Column(TINYINT(1), nullable=False, server_default=text("0"))
    xp_reward = Column(INTEGER(11), nullable=False, server_default=text("0"))
    completion_message = Column(String(80), nullable=False)


class Race(Base):
    __tablename__ = 'races'

    race_id = Column(TINYINT(3), primary_key=True)
    race_name = Column(String(15), nullable=False, unique=True)
    race_description = Column(String(64))


class RemortUpgrade(Base):
    __tablename__ = 'remort_upgrades'

    upgrade_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False, unique=True, server_default=text("''"))
    renown_cost = Column(SMALLINT(6), nullable=False)
    max_value = Column(SMALLINT(6), nullable=False)


class Season(Base):
    __tablename__ = 'seasons'

    season_id = Column(INTEGER(11), primary_key=True)
    is_active = Column(TINYINT(4), nullable=False)
    effective_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    expiration_date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))



t_accounts_account_upgrades = Table(
    'accounts_account_upgrades', metadata,
    Column('account_upgrades_id', ForeignKey('account_upgrades.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('account_id', ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('amount', MEDIUMINT(4), nullable=False)
)




class News(Base):
    __tablename__ = 'news'

    news_id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    subject = Column(String(64), nullable=False, server_default=text("''"))
    body = Column(Text, nullable=False)

    account = relationship('Account')


class Player(Base):
    __tablename__ = 'players'

    id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String(15), nullable=False, unique=True, server_default=text("''"))
    create_ident = Column(String(10), nullable=False, server_default=text("''"))
    last_isp = Column(String(30), nullable=False, server_default=text("''"))
    description = Column(String(240))
    title = Column(String(45), nullable=False, server_default=text("''"))
    poofin = Column(String(80), nullable=False, server_default=text("''"))
    poofout = Column(String(80), nullable=False, server_default=text("''"))
    bankacc = Column(INTEGER(11), nullable=False)
    logon_delay = Column(SMALLINT(6), nullable=False)
    true_level = Column(INTEGER(11), nullable=False)
    renown = Column(INTEGER(11), nullable=False)
    prompt = Column(String(42), nullable=False, server_default=text("''"))
    remorts = Column(INTEGER(11), nullable=False)
    favors = Column(INTEGER(11), nullable=False)
    birth = Column(INTEGER(11), nullable=False)
    logon = Column(INTEGER(11), nullable=False)
    online = Column(INTEGER(11))
    logout = Column(INTEGER(11), nullable=False)
    bound_room = Column(INTEGER(11), nullable=False)
    load_room = Column(INTEGER(11), nullable=False)
    wimpy = Column(SMALLINT(6))
    invstart_level = Column(INTEGER(11))
    color_scheme = Column(SMALLINT(6))
    sex = Column(TINYINT(3), nullable=False)
    race_id = Column(ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    class_id = Column(ForeignKey('classes.class_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    level = Column(INTEGER(11), nullable=False)
    weight = Column(SMALLINT(6), nullable=False)
    height = Column(SMALLINT(6), nullable=False)
    align = Column(SMALLINT(6), nullable=False)
    comm = Column(SMALLINT(6), nullable=False)
    karma = Column(SMALLINT(6), nullable=False)
    experience_points = Column(INTEGER(11), nullable=False)
    money = Column(INTEGER(11), nullable=False)
    fg_color = Column(SMALLINT(6), nullable=False, server_default=text("0"))
    bg_color = Column(SMALLINT(6), nullable=False, server_default=text("0"))
    login_failures = Column(SMALLINT(6), nullable=False)
    create_haddr = Column(INTEGER(11), nullable=False)
    auto_level = Column(INTEGER(11), nullable=False, server_default=text("0"))
    login_fail_haddr = Column(INTEGER(11))
    last_haddr = Column(INTEGER(11))
    last_ident = Column(String(10), server_default=text("''"))
    load_room_next = Column(INTEGER(11))
    load_room_next_expires = Column(INTEGER(11))
    aggro_until = Column(INTEGER(11))
    inn_limit = Column(SMALLINT(6), nullable=False)
    held_xp = Column(INTEGER(11))
    last_isp_change = Column(INTEGER(11))
    perm_hit_pts = Column(INTEGER(11), nullable=False)
    perm_move_pts = Column(INTEGER(11), nullable=False)
    perm_spell_pts = Column(INTEGER(11), nullable=False)
    perm_favor_pts = Column(INTEGER(11), nullable=False)
    curr_hit_pts = Column(INTEGER(11), nullable=False)
    curr_move_pts = Column(INTEGER(11), nullable=False)
    curr_spell_pts = Column(INTEGER(11), nullable=False)
    curr_favor_pts = Column(INTEGER(11), nullable=False)
    init_strength = Column(TINYINT(4), nullable=False)
    init_agility = Column(TINYINT(4), nullable=False)
    init_endurance = Column(TINYINT(4), nullable=False)
    init_perception = Column(TINYINT(4), nullable=False)
    init_focus = Column(TINYINT(4), nullable=False)
    init_willpower = Column(TINYINT(4), nullable=False)
    curr_strength = Column(TINYINT(4), nullable=False)
    curr_agility = Column(TINYINT(4), nullable=False)
    curr_endurance = Column(TINYINT(4), nullable=False)
    curr_perception = Column(TINYINT(4), nullable=False)
    curr_focus = Column(TINYINT(4), nullable=False)
    curr_willpower = Column(TINYINT(4), nullable=False)
    is_deleted = Column(TINYINT(4), nullable=False, server_default=text("0"))
    deaths = Column(INTEGER(11), nullable=False, server_default=text("0"))
    total_renown = Column(INTEGER(11), nullable=False, server_default=text("0"))
    quests_completed = Column(INTEGER(11), nullable=False, server_default=text("0"))
    challenges_completed = Column(INTEGER(11), nullable=False, server_default=text("0"))

    account = relationship('Account')
    _class = relationship('Class')
    race = relationship('Race')


t_player_accounts = Table(
    'player_accounts', metadata,
    Column('account_id', ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
)



t_player_player_flags = Table(
    'player_player_flags', metadata,
    Column('flag_id', ForeignKey('player_flags.flag_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', INTEGER(11), nullable=False)
)


t_player_quests = Table(
    'player_quests', metadata,
    Column('quest_id', ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', INTEGER(11), nullable=False)
)


t_player_remort_upgrades = Table(
    'player_remort_upgrades', metadata,
    Column('upgrade_id', ForeignKey('remort_upgrades.upgrade_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('value', INTEGER(11), nullable=False)
)
