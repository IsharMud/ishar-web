# coding: utf-8
from sqlalchemy import Column, Float, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AccountUpgrade(Base):
    __tablename__ = 'account_upgrades'

    id = Column(TINYINT(4), primary_key=True)
    cost = Column(MEDIUMINT(4), nullable=False)
    description = Column(String(400), nullable=False)
    name = Column(String(80), nullable=False, unique=True)
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
    banned_until = Column(TIMESTAMP)
    bugs_reported = Column(INTEGER(11), nullable=False, server_default=text("0"))


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


class Force(Base):
    __tablename__ = 'forces'

    id = Column(INTEGER(11), primary_key=True)
    force_name = Column(String(255), unique=True)

    spells = relationship('SpellInfo', secondary='spell_forces')


class GlobalEvent(Base):
    __tablename__ = 'global_event'

    event_type = Column(TINYINT(4), primary_key=True, unique=True)
    start_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    end_time = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    event_name = Column(String(20), nullable=False)
    event_desc = Column(String(40), nullable=False)
    xp_bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    shop_bonus = Column(TINYINT(4), nullable=False)
    celestial_luck = Column(TINYINT(1), nullable=False, server_default=text("0"))


class PlayerFlag(Base):
    __tablename__ = 'player_flags'

    flag_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)


class PlayerQuestStep(Base):
    __tablename__ = 'player_quest_steps'

    player_id = Column(INTEGER(11), primary_key=True, nullable=False)
    step_id = Column(TINYINT(4), primary_key=True, nullable=False, index=True)
    num_collected = Column(TINYINT(1), nullable=False)


class Quest(Base):
    __tablename__ = 'quests'

    quest_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False, unique=True, server_default=text("''"))
    display_name = Column(String(30), nullable=False)
    completion_message = Column(String(700), nullable=False)
    min_level = Column(TINYINT(4), nullable=False, server_default=text("1"))
    max_level = Column(TINYINT(4), nullable=False, server_default=text("20"))
    repeatable = Column(TINYINT(1), nullable=False, server_default=text("0"))
    description = Column(String(512), nullable=False, server_default=text("'No description available.'"))
    prerequisite = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    class_restrict = Column(TINYINT(4), nullable=False, server_default=text("-1"))
    quest_intro = Column(String(2000), nullable=False, server_default=text("''"))
    quest_source = Column(INTEGER(10))
    quest_return = Column(INTEGER(10))

    parents = relationship(
        'Quest',
        secondary='quest_prereqs',
        primaryjoin='Quest.quest_id == quest_prereqs.c.quest_id',
        secondaryjoin='Quest.quest_id == quest_prereqs.c.required_quest'
    )


class Race(Base):
    __tablename__ = 'races'

    race_id = Column(INTEGER(11), primary_key=True)
    symbol = Column(String(100), server_default=text("''"))
    display_name = Column(String(25), server_default=text("''"))
    folk_name = Column(String(25), server_default=text("''"))
    default_movement = Column(String(10), server_default=text("''"))
    description = Column(String(80), server_default=text("''"))
    default_height = Column(SMALLINT(6), server_default=text("0"))
    default_weight = Column(SMALLINT(6), server_default=text("0"))
    bonus_fortitude = Column(SMALLINT(6), server_default=text("0"))
    bonus_reflex = Column(SMALLINT(6), server_default=text("0"))
    bonus_resilience = Column(SMALLINT(6), server_default=text("0"))
    listen_sound = Column(String(80), server_default=text("''"))
    height_bonus = Column(SMALLINT(6), server_default=text("0"))
    weight_bonus = Column(SMALLINT(6), server_default=text("0"))
    short_description = Column(String(80), server_default=text("''"))
    long_description = Column(String(512), server_default=text("''"))
    attack_noun = Column(String(25), server_default=text("''"))
    attack_type = Column(SMALLINT(6), server_default=text("0"))
    vulnerabilities = Column(Text, server_default=text("''"))
    susceptibilities = Column(Text, server_default=text("''"))
    resistances = Column(Text, server_default=text("''"))
    immunities = Column(Text, server_default=text("''"))
    additional_str = Column(SMALLINT(6), server_default=text("0"))
    additional_agi = Column(SMALLINT(6), server_default=text("0"))
    additional_end = Column(SMALLINT(6), server_default=text("0"))
    additional_per = Column(SMALLINT(6), server_default=text("0"))
    additional_foc = Column(SMALLINT(6), server_default=text("0"))
    additional_wil = Column(SMALLINT(6), server_default=text("0"))
    is_playable = Column(TINYINT(1), server_default=text("0"))
    is_humanoid = Column(TINYINT(1), nullable=False, server_default=text("1"))
    is_invertebrae = Column(TINYINT(1), nullable=False, server_default=text("0"))
    is_flying = Column(TINYINT(1), nullable=False, server_default=text("0"))
    is_swimming = Column(TINYINT(1), nullable=False, server_default=text("0"))
    darkvision = Column(TINYINT(4), nullable=False, server_default=text("0"))
    see_invis = Column(TINYINT(1), nullable=False, server_default=text("0"))
    is_walking = Column(TINYINT(1), nullable=False, server_default=text("1"))
    endure_heat = Column(TINYINT(1), nullable=False, server_default=text("0"))
    endure_cold = Column(TINYINT(1), nullable=False, server_default=text("0"))
    is_undead = Column(TINYINT(1), nullable=False, server_default=text("0"))


class RemortUpgrade(Base):
    __tablename__ = 'remort_upgrades'

    upgrade_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False, unique=True, server_default=text("''"))
    renown_cost = Column(SMALLINT(6), nullable=False)
    max_value = Column(SMALLINT(6), nullable=False)
    scale = Column(TINYINT(4), nullable=False, server_default=text("10"))
    display_name = Column(String(30), nullable=False)
    can_buy = Column(TINYINT(1), nullable=False, server_default=text("1"))
    bonus = Column(TINYINT(4), nullable=False, server_default=text("1"))
    survival_scale = Column(TINYINT(4), nullable=False)
    survival_renown_cost = Column(TINYINT(4), nullable=False)


class Season(Base):
    __tablename__ = 'seasons'

    season_id = Column(INTEGER(11), primary_key=True)
    is_active = Column(TINYINT(4), nullable=False)
    effective_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    expiration_date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    average_essence_gain = Column(Float, nullable=False, server_default=text("0"))
    average_remorts = Column(Float, nullable=False, server_default=text("0"))
    max_essence_gain = Column(INTEGER(11), nullable=False, server_default=text("0"))
    max_remorts = Column(INTEGER(11), nullable=False, server_default=text("0"))
    season_leader_account = Column(INTEGER(11), nullable=False, server_default=text("0"))
    seasonal_leader_name = Column(Text, nullable=False, server_default=text("'Tyler'"))


class Skill(Base):
    __tablename__ = 'skills'

    skill_id = Column(INTEGER(11), primary_key=True)


class SpellFlag(Base):
    __tablename__ = 'spell_flags'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))

    spells = relationship('SpellInfo', secondary='spells_spell_flags')


class SpellInfo(Base):
    __tablename__ = 'spell_info'

    id = Column(INTEGER(11), primary_key=True)
    enum_symbol = Column(String(255), nullable=False)
    func_name = Column(String(255))
    skill_name = Column(Text)
    min_posn = Column(INTEGER(11))
    min_use = Column(INTEGER(11))
    spell_breakpoint = Column(INTEGER(11))
    held_cost = Column(INTEGER(11))
    wearoff_msg = Column(Text)
    chant_text = Column(Text)
    difficulty = Column(INTEGER(11))
    rate = Column(INTEGER(11))
    notice_chance = Column(INTEGER(11))
    appearance = Column(Text)
    component_type = Column(INTEGER(11))
    component_value = Column(INTEGER(11))
    scale = Column(INTEGER(11))
    mod_stat_1 = Column(INTEGER(11))
    mod_stat_2 = Column(INTEGER(11))
    is_spell = Column(TINYINT(1))
    is_skill = Column(TINYINT(1))
    is_type = Column(TINYINT(1))
    decide_func = Column(Text, nullable=False)


t_spell_info_bck = Table(
    'spell_info_bck', metadata,
    Column('id', INTEGER(11), nullable=False),
    Column('enum_symbol', String(255), nullable=False),
    Column('func_name', String(255)),
    Column('skill_name', Text),
    Column('min_posn', INTEGER(11)),
    Column('min_use', INTEGER(11)),
    Column('spell_breakpoint', INTEGER(11)),
    Column('held_cost', INTEGER(11)),
    Column('wearoff_msg', Text),
    Column('chant_text', Text),
    Column('difficulty', INTEGER(11)),
    Column('rate', INTEGER(11)),
    Column('notice_chance', INTEGER(11)),
    Column('appearance', Text),
    Column('component_type', INTEGER(11)),
    Column('component_value', INTEGER(11)),
    Column('scale', INTEGER(11)),
    Column('mod_stat_1', INTEGER(11)),
    Column('mod_stat_2', INTEGER(11)),
    Column('is_spell', TINYINT(1)),
    Column('is_skill', TINYINT(1)),
    Column('is_type', TINYINT(1)),
    Column('decide_func', Text, nullable=False)
)


class AccountsAccountUpgrade(Base):
    __tablename__ = 'accounts_account_upgrades'

    account_upgrades_id = Column(ForeignKey('account_upgrades.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    amount = Column(MEDIUMINT(4), nullable=False)

    account = relationship('Account')
    account_upgrades = relationship('AccountUpgrade')


class AccountsConfigurationOption(Base):
    __tablename__ = 'accounts_configuration_options'

    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
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


class PlayerQuest(Base):
    __tablename__ = 'player_quests'

    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    player_id = Column(INTEGER(11), primary_key=True, nullable=False, index=True)
    status = Column(TINYINT(11), nullable=False)
    last_completed_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    num_completed = Column(TINYINT(4), nullable=False, server_default=text("0"))

    quest = relationship('Quest')


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


t_quest_prereqs = Table(
    'quest_prereqs', metadata,
    Column('quest_id', ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('required_quest', ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class QuestReward(Base):
    __tablename__ = 'quest_rewards'

    reward_num = Column(INTEGER(11), primary_key=True, nullable=False)
    reward_type = Column(TINYINT(2), nullable=False)
    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    class_restrict = Column(TINYINT(4), nullable=False, server_default=text("-1"))

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


t_races_skills = Table(
    'races_skills', metadata,
    Column('race_id', ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('skill_id', ForeignKey('spell_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('level', TINYINT(4), nullable=False)
)


t_racial_affinities = Table(
    'racial_affinities', metadata,
    Column('race_id', ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('force_id', ForeignKey('forces.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('affinity_type', TINYINT(4), nullable=False)
)


t_spell_forces = Table(
    'spell_forces', metadata,
    Column('spell_id', ForeignKey('spell_info.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('force_id', ForeignKey('forces.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Index('spell_id_2', 'spell_id', 'force_id', unique=True)
)


t_spells_spell_flags = Table(
    'spells_spell_flags', metadata,
    Column('spell_id', ForeignKey('spell_info.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('flag_id', ForeignKey('spell_flags.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class KillMemory(Base):
    __tablename__ = 'kill_memory'
    __table_args__ = (
        Index('player_id', 'player_id', 'kill_memory_set', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'))
    kill_memory_set = Column(INTEGER(11))
    scratch = Column(SMALLINT(6))
    nonzero = Column(SMALLINT(6))
    total = Column(INTEGER(11))

    player = relationship('Player')


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
    Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True),
    Column('class_id', TINYINT(4), nullable=False),
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


class PlayerPlayerFlag(Base):
    __tablename__ = 'player_player_flags'

    flag_id = Column(ForeignKey('player_flags.flag_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(INTEGER(11), nullable=False)

    flag = relationship('PlayerFlag')
    player = relationship('Player')


class PlayerRemortUpgrade(Base):
    __tablename__ = 'player_remort_upgrades'

    upgrade_id = Column(ForeignKey('remort_upgrades.upgrade_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(INTEGER(11), nullable=False)
    essence_perk = Column(TINYINT(4), nullable=False, server_default=text("0"))

    player = relationship('Player')
    upgrade = relationship('RemortUpgrade')


class PlayerSkill(Base):
    __tablename__ = 'player_skills'

    skill_id = Column(ForeignKey('spell_info.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    skill_level = Column(TINYINT(11), nullable=False)

    player = relationship('Player')
    skill = relationship('SpellInfo')


class KillMemoryBucket(Base):
    __tablename__ = 'kill_memory_buckets'

    id = Column(INTEGER(11), primary_key=True)
    kill_memory_id = Column(ForeignKey('kill_memory.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    bucket_index = Column(SMALLINT(6))
    value = Column(SMALLINT(6))

    kill_memory = relationship('KillMemory')
