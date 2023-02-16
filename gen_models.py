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
    account_gift = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))

    players = relationship('Player', secondary='player_accounts')


class AffectFlag(Base):
    __tablename__ = 'affect_flags'

    flag_id = Column(TINYINT(4), primary_key=True)
    name = Column(String(30), nullable=False, unique=True)


class Board(Base):
    __tablename__ = 'boards'

    board_id = Column(TINYINT(4), primary_key=True)
    board_name = Column(String(15), nullable=False)


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


class Condition(Base):
    __tablename__ = 'conditions'

    condition_id = Column(TINYINT(4), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)


class ConfigurationOption(Base):
    __tablename__ = 'configuration_options'

    configuration_option_id = Column(TINYINT(4), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    is_display = Column(TINYINT(1), nullable=False, server_default=text("0"))


class GlobalEvent(Base):
    __tablename__ = 'global_event'

    event_type = Column(TINYINT(4), primary_key=True, unique=True)
    start_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    end_time = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    event_name = Column(String(20), nullable=False)
    event_desc = Column(String(40), nullable=False)
    xp_bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    shop_bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    celestial_luck = Column(TINYINT(1), nullable=False, server_default=text("0"))


t_objects = Table(
    'objects', metadata,
    Column('vnum', INTEGER(11), nullable=False),
    Column('seed', SMALLINT(6), nullable=False),
    Column('timer', SMALLINT(6), nullable=False),
    Column('otype', TINYINT(4), nullable=False),
    Column('equipped', TINYINT(4), nullable=False),
    Column('size', SMALLINT(6), nullable=False),
    Column('weight', INTEGER(11), nullable=False),
    Column('value', INTEGER(11), nullable=False),
    Column('val0', INTEGER(11), nullable=False),
    Column('val1', INTEGER(11), nullable=False),
    Column('val2', INTEGER(11), nullable=False),
    Column('val3', INTEGER(11), nullable=False),
    Column('state', INTEGER(11), nullable=False),
    Column('min_level', TINYINT(4), nullable=False),
    Column('loaded_on', INTEGER(11), nullable=False)
)


class PlayerFlag(Base):
    __tablename__ = 'player_flags'

    flag_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)


class Quest(Base):
    __tablename__ = 'quests'

    quest_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False, unique=True, server_default=text("''"))
    display_name = Column(String(30), nullable=False)
    renown_reward = Column(TINYINT(1), nullable=False, server_default=text("0"))
    xp_reward = Column(INTEGER(11), nullable=False, server_default=text("0"))
    completion_message = Column(String(80), nullable=False)
    cash_reward = Column(INTEGER(11), nullable=False, server_default=text("0"))
    min_level = Column(TINYINT(4), nullable=False, server_default=text("1"))
    max_level = Column(TINYINT(4), nullable=False, server_default=text("20"))
    repeatable = Column(TINYINT(1), nullable=False, server_default=text("0"))
    description = Column(String(512), nullable=False, server_default=text("'No description available.'"))
    prerequisite = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    skill_reward = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    next_quest = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    class_restrict = Column(TINYINT(4), nullable=False, server_default=text("-1"))
    align_reward = Column(INTEGER(11), nullable=False, server_default=text("0"))
    quest_intro = Column(String(1600), nullable=False, server_default=text("''"))


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
    scale = Column(TINYINT(4), nullable=False, server_default=text("10"))
    display_name = Column(String(30), nullable=False)
    can_buy = Column(TINYINT(1), nullable=False, server_default=text("1"))
    bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    survival_scale = Column(TINYINT(4), nullable=False)
    survival_renown_cost = Column(TINYINT(4), nullable=False)


class Season(Base):
    __tablename__ = 'seasons'

    season_id = Column(INTEGER(11), primary_key=True)
    is_active = Column(TINYINT(4), nullable=False)
    effective_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    expiration_date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))


class Skill(Base):
    __tablename__ = 'skills'

    skill_id = Column(INTEGER(11), primary_key=True)
    class_id = Column(INTEGER(11), nullable=False)
    max_value = Column(INTEGER(11), nullable=False)
    difficulty = Column(INTEGER(11), nullable=False)


class AccountsAccountUpgrade(Base):
    __tablename__ = 'accounts_account_upgrades'

    account_upgrades_id = Column(ForeignKey('account_upgrades.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    amount = Column(MEDIUMINT(4), nullable=False)

    account = relationship('Account')
    account_upgrades = relationship('AccountUpgrade')


class AccountsConfigurationOption(Base):
    __tablename__ = 'accounts_configuration_options'

    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    configuration_option_id = Column(ForeignKey('configuration_options.configuration_option_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(String(76), nullable=False)

    account = relationship('Account')
    configuration_option = relationship('ConfigurationOption')


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
    true_level = Column(TINYINT(3), nullable=False)
    renown = Column(TINYINT(3), nullable=False)
    remorts = Column(TINYINT(3), nullable=False)
    favors = Column(TINYINT(3), nullable=False)
    online = Column(INTEGER(11))
    bound_room = Column(INTEGER(11), nullable=False)
    load_room = Column(INTEGER(11), nullable=False)
    invstart_level = Column(INTEGER(11))
    login_failures = Column(SMALLINT(6), nullable=False)
    create_haddr = Column(INTEGER(11), nullable=False)
    login_fail_haddr = Column(INTEGER(11))
    last_haddr = Column(INTEGER(11))
    last_ident = Column(String(10), server_default=text("''"))
    load_room_next = Column(INTEGER(11))
    load_room_next_expires = Column(INTEGER(11))
    aggro_until = Column(INTEGER(11))
    inn_limit = Column(SMALLINT(6), nullable=False)
    held_xp = Column(INTEGER(11))
    last_isp_change = Column(INTEGER(11))
    is_deleted = Column(TINYINT(4), nullable=False, server_default=text("0"))
    deaths = Column(SMALLINT(5), nullable=False, server_default=text("0"))
    total_renown = Column(SMALLINT(5), nullable=False, server_default=text("0"))
    quests_completed = Column(SMALLINT(5), nullable=False, server_default=text("0"))
    challenges_completed = Column(SMALLINT(5), nullable=False, server_default=text("0"))
    game_type = Column(TINYINT(4), nullable=False, server_default=text("0"))
    birth = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    logon = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    logout = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))

    account = relationship('Account')


class QuestReward(Base):
    __tablename__ = 'quest_rewards'

    reward_num = Column(INTEGER(11), primary_key=True, nullable=False)
    reward_type = Column(TINYINT(2), nullable=False)
    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)

    quest = relationship('Quest')


class QuestStep(Base):
    __tablename__ = 'quest_steps'

    step_id = Column(TINYINT(4), primary_key=True)
    step_type = Column(TINYINT(4), nullable=False)
    target = Column(INTEGER(11), nullable=False)
    num_required = Column(INTEGER(11), nullable=False)
    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    time_limit = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    mystify = Column(TINYINT(1), nullable=False, server_default=text("0"))
    mystify_text = Column(String(80), nullable=False, server_default=text("''"))

    quest = relationship('Quest')


t_player_accounts = Table(
    'player_accounts', metadata,
    Column('account_id', ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
)


class PlayerAffectFlag(Base):
    __tablename__ = 'player_affect_flags'

    affect_flag_id = Column(ForeignKey('affect_flags.flag_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    expires = Column(INTEGER(11), nullable=False)
    flag_value = Column(TINYINT(4), nullable=False)
    bits = Column(INTEGER(11), nullable=False)
    location_1 = Column(INTEGER(11), nullable=False)
    mod_1 = Column(INTEGER(11), nullable=False)
    location_2 = Column(INTEGER(11), nullable=False)
    mod_2 = Column(INTEGER(11), nullable=False)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)

    affect_flag = relationship('AffectFlag')
    player = relationship('Player')


class PlayerBoard(Base):
    __tablename__ = 'player_boards'

    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    board_id = Column(ForeignKey('boards.board_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    last_read = Column(TINYINT(4), nullable=False)
    last_read_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))

    board = relationship('Board')
    player = relationship('Player')


t_player_common = Table(
    'player_common', metadata,
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('class_id', ForeignKey('classes.class_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('race_id', ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('sex', TINYINT(4), nullable=False, server_default=text("0")),
    Column('level', TINYINT(3), nullable=False),
    Column('weight', SMALLINT(5), nullable=False),
    Column('height', SMALLINT(5), nullable=False),
    Column('comm_points', SMALLINT(6), nullable=False),
    Column('alignment', SMALLINT(6), nullable=False),
    Column('strength', TINYINT(3), nullable=False),
    Column('agility', TINYINT(3), nullable=False),
    Column('endurance', TINYINT(3), nullable=False),
    Column('perception', TINYINT(3), nullable=False),
    Column('focus', TINYINT(3), nullable=False),
    Column('willpower', TINYINT(3), nullable=False),
    Column('init_strength', TINYINT(3), nullable=False),
    Column('init_agility', TINYINT(3), nullable=False),
    Column('init_endurance', TINYINT(3), nullable=False),
    Column('init_perception', TINYINT(3), nullable=False),
    Column('init_focus', TINYINT(3), nullable=False),
    Column('init_willpower', TINYINT(3), nullable=False),
    Column('perm_hit_pts', SMALLINT(6), nullable=False),
    Column('perm_move_pts', SMALLINT(6), nullable=False),
    Column('perm_spell_pts', SMALLINT(6), nullable=False),
    Column('perm_favor_pts', SMALLINT(6), nullable=False),
    Column('curr_hit_pts', SMALLINT(6), nullable=False),
    Column('curr_move_pts', SMALLINT(6), nullable=False),
    Column('curr_spell_pts', SMALLINT(6), nullable=False),
    Column('curr_favor_pts', SMALLINT(6), nullable=False),
    Column('experience', INTEGER(11), nullable=False),
    Column('gold', MEDIUMINT(9), nullable=False),
    Column('karma', MEDIUMINT(9), nullable=False)
)


class PlayerCondition(Base):
    __tablename__ = 'player_conditions'

    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    condition_id = Column(ForeignKey('conditions.condition_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(SMALLINT(6), nullable=False)

    condition = relationship('Condition')
    player = relationship('Player')


class PlayerConfigurationOption(Base):
    __tablename__ = 'player_configuration_options'

    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    configuration_option_id = Column(ForeignKey('configuration_options.configuration_option_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(String(76), nullable=False)

    configuration_option = relationship('ConfigurationOption')
    player = relationship('Player')


class PlayerKillBucket(Base):
    __tablename__ = 'player_kill_buckets'

    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    bucket_id = Column(INTEGER(11), primary_key=True)
    bucket_data = Column(INTEGER(11), nullable=False)

    player = relationship('Player')


class PlayerPlayerFlag(Base):
    __tablename__ = 'player_player_flags'

    flag_id = Column(ForeignKey('player_flags.flag_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(INTEGER(11), nullable=False)

    flag = relationship('PlayerFlag')
    player = relationship('Player')


class PlayerQuestStep(Base):
    __tablename__ = 'player_quest_steps'

    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    step_id = Column(ForeignKey('quest_steps.step_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    num_collected = Column(TINYINT(1), nullable=False)

    player = relationship('Player')
    step = relationship('QuestStep')


class PlayerQuest(Base):
    __tablename__ = 'player_quests'

    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    status = Column(TINYINT(11), nullable=False)
    last_completed_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    num_completed = Column(TINYINT(4), nullable=False, server_default=text("0"))

    player = relationship('Player')
    quest = relationship('Quest')


class PlayerRemortUpgrade(Base):
    __tablename__ = 'player_remort_upgrades'

    upgrade_id = Column(ForeignKey('remort_upgrades.upgrade_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(INTEGER(11), nullable=False)
    essence_perk = Column(TINYINT(1), nullable=False, server_default=text("0"))

    player = relationship('Player')
    upgrade = relationship('RemortUpgrade')


class PlayerSkill(Base):
    __tablename__ = 'player_skills'

    skill_id = Column(INTEGER(11), primary_key=True, nullable=False)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    skill_level = Column(TINYINT(11), nullable=False)

    player = relationship('Player')
