"""Database classes/models"""
import datetime
from functools import cached_property
from flask import url_for
from flask_login import UserMixin
from passlib.hash import md5_crypt
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from mud_secret import ALIGNMENTS, IMM_LEVELS
from database import Base, db_session
import delta


class Account(Base, UserMixin):
    """Account used to log in to the website and MUD in-game"""
    __tablename__ = 'accounts'

    account_id = Column(INTEGER(11), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    seasonal_points = Column(MEDIUMINT(4), nullable=False, server_default=FetchedValue())
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(36), nullable=False)
    create_isp = Column(String(25), nullable=False)
    last_isp = Column(String(25), nullable=False)
    create_ident = Column(String(25), nullable=False)
    last_ident = Column(String(25), nullable=False)
    create_haddr = Column(INTEGER(11), nullable=False)
    last_haddr = Column(INTEGER(11), nullable=False)
    account_name = Column(String(25), nullable=False, unique=True)

    players = relationship('Player', backref='account')

    def change_password(self, new_password):
        """Method to change an account password"""
        try:
            self.password = md5_crypt.hash(new_password)
            db_session.commit()
            return True
        except Exception as err:
            print(err)
        return False

    def check_password(self, password):
        """Method to check an account password"""
        return md5_crypt.verify(password, self.password)

    def get_id(self):
        """flask-login account ID"""
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
    def created(self):
        """Timedelta since account created"""
        return datetime.datetime.utcnow() - self.created_at

    @cached_property
    def created_ago(self):
        """Stringified approximate timedelta since account created"""
        return delta.stringify(self.created) + ' ago'

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
        return f'<Account> "{self.account_name}" (ID: {self.account_id})'


class AccountUpgrade(Base):
    """Account upgrades that are available to accounts"""
    __tablename__ = 'account_upgrades'

    id = Column(TINYINT(4), primary_key=True)
    cost = Column(MEDIUMINT(4), nullable=False)
    description = Column(String(200), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    max_value = Column(MEDIUMINT(4), nullable=False, server_default=FetchedValue())
    scale = Column(TINYINT(4), nullable=False, server_default=FetchedValue())
    is_disabled = Column(TINYINT(1), nullable=False, server_default=FetchedValue())

    accounts_upgrade = relationship('AccountsUpgrade', backref='upgrade')

    def __repr__(self):
        return f'<AccountUpgrade> "{self.name}" ({self.id}) / ' \
               f'Cost: {self.cost} / Max Value: {self.max_value}'


class AccountsUpgrade(Base):
    """Account upgrade associated with account, and the level of upgrade"""
    __tablename__ = 'accounts_account_upgrades'

    account_upgrades_id = Column(ForeignKey('account_upgrades.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    amount = Column(MEDIUMINT(4), nullable=False)

    account = relationship('Account', backref='upgrades')

    def __repr__(self):
        return f'<AccountsUpgrade> "{self.upgrade.name}" ' \
               f'({self.account_upgrades_id}) @ ' \
               f'<Account> "{self.account.account_name}" ' \
               f'({self.account_id}) / ' \
               f'Amount: {self.amount}'


class Challenge(Base):
    """Challenge along with the in-game mobile ("mob")/target number (mob_vnum),
        as well as level/group requirements, and tier"""
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
    winner_desc = Column(String(80), nullable=False, server_default=FetchedValue())
    mob_name = Column(String(30), nullable=False)
    is_active = Column(TINYINT(1), nullable=False, server_default=FetchedValue())

    @cached_property
    def is_completed(self):
        """Boolean whether challenge is completed"""
        if self.winner_desc != '':
            return True
        return False

    def __repr__(self):
        return f'<Challenge> "{self.mob_name}" ({self.challenge_id}) / ' \
               f'Active: {self.is_active} / Reward: "{self.reward_tier}" ' \
               f'({self.adj_tier}) / winner_desc: "{self.winner_desc}"'


class News(Base):
    """News post for the main/welcome page"""
    __tablename__ = 'news'

    news_id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    subject = Column(String(64), nullable=False, server_default=FetchedValue())
    body = Column(Text, nullable=False)

    account = relationship('Account')

    def __repr__(self):
        return f'<News> "{self.subject}" ({self.news_id}) / ' \
               f'by "{self.account.account_name}" / at "{self.created_at}"'


class PlayerClass(Base):
    """Playable character class such as warrior, rogue, or casters..."""
    __tablename__ = 'classes'

    class_id = Column(TINYINT(3), primary_key=True)
    class_name = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    class_display = Column(String(32))
    class_description = Column(String(64))

    def __repr__(self):
        return f'<PlayerClass> "{self.class_name}" ({self.class_id})'


class PlayerRace(Base):
    """Playable character race, such as elf, gnome, human, etc."""
    __tablename__ = 'races'

    race_id = Column(TINYINT(3), primary_key=True)
    race_name = Column(String(15), nullable=False, unique=True)
    race_description = Column(String(64))

    def __repr__(self):
        return f'<PlayerRace> "{self.race_name}" ({self.race_id})'


class Quest(Base):
    """Quest that can be achieved, and its rewards"""
    __tablename__ = 'quests'

    quest_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False, unique=True, server_default=FetchedValue())
    display_name = Column(String(30), nullable=False)
    is_major = Column(TINYINT(1), nullable=False, server_default=FetchedValue())
    xp_reward = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    completion_message = Column(String(80), nullable=False)

    def __repr__(self):
        return f'<Quest> "{self.name}" ({self.quest_id}) / ' \
               f'"{self.display_name}" / XP: {self.xp_reward}'


class PlayerQuest(Base):
    """Player Quest database class
    Quest associated with players completion"""
    __tablename__ = 'player_quests'

    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    value = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    quest = relationship('Quest')

    def __repr__(self):
        return f'<PlayerQuest> "{self.quest.name}" ({self.quest_id}) @ ' \
               f'<Player> "{self.player.name}" ({self.player_id}) ' \
               f'/ Value: {self.value}'


class RemortUpgrade(Base):
    """Remort Upgrades database class
    Remort upgrade available to players, as well as the renown cost and max value"""
    __tablename__ = 'remort_upgrades'

    upgrade_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False, unique=True, server_default=FetchedValue())
    renown_cost = Column(SMALLINT(6), nullable=False)
    max_value = Column(SMALLINT(6), nullable=False)

    remort_upgrades = relationship('PlayerRemortUpgrade', backref='remort_upgrade')

    def __repr__(self):
        return f'<RemortUpgrade> "{self.name}" ({self.upgrade_id}) / ' \
               f'Cost: {self.renown_cost} / Max: {self.max_value}'


class PlayerRemortUpgrade(Base):
    """Remort upgrade associated with player, and the level of upgrade"""
    __tablename__ = 'player_remort_upgrades'

    upgrade_id = Column(ForeignKey('remort_upgrades.upgrade_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    value = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    player = relationship('Player', backref='remort_upgrades')

    def __repr__(self):
        return f'<PlayerRemortUpgrade> "{self.remort_upgrade.name}" ' \
               f'({self.upgrade_id}) @ <Player> "{self.player.name}" ' \
               f'({self.player_id}) / Value: {self.value}'


class Season(Base):
    """In-game cyclical season detail and dates"""
    __tablename__ = 'seasons'

    season_id = Column(INTEGER(11), primary_key=True)
    is_active = Column(TINYINT(4), nullable=False)
    effective_date = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    expiration_date = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())

    @property
    def effective(self):
        """Stringified approximate timedelta since season started"""
        return delta.stringify(datetime.datetime.utcnow() - self.effective_date)

    @property
    def expires(self):
        """Stringified approximate timedelta until season ends"""
        return delta.stringify(self.expiration_date - datetime.datetime.utcnow())

    def __repr__(self):
        return f'<Season> ID {self.season_id} / Active: {self.is_active} / ' \
               f'Effective: {self.effective_date} ("{self.effective}") - ' \
               f'Expires: {self.expiration_date} ("{self.expires}")'


class Player(Base):
    """
    Player database class
    An in-game player, which belongs to an account
    """
    __tablename__ = 'players'

    id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    create_ident = Column(String(10), nullable=False, server_default=FetchedValue())
    last_isp = Column(String(30), nullable=False, server_default=FetchedValue())
    description = Column(String(240))
    title = Column(String(45), nullable=False, server_default=FetchedValue())
    poofin = Column(String(80), nullable=False, server_default=FetchedValue())
    poofout = Column(String(80), nullable=False, server_default=FetchedValue())
    bankacc = Column(INTEGER(11), nullable=False)
    logon_delay = Column(SMALLINT(6), nullable=False)
    true_level = Column(INTEGER(11), nullable=False)
    renown = Column(INTEGER(11), nullable=False)
    prompt = Column(String(42), nullable=False, server_default=FetchedValue())
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
    fg_color = Column(SMALLINT(6), nullable=False, server_default=FetchedValue())
    bg_color = Column(SMALLINT(6), nullable=False, server_default=FetchedValue())
    login_failures = Column(SMALLINT(6), nullable=False)
    create_haddr = Column(INTEGER(11), nullable=False)
    auto_level = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    login_fail_haddr = Column(INTEGER(11))
    last_haddr = Column(INTEGER(11))
    last_ident = Column(String(10), server_default=FetchedValue())
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
    is_deleted = Column(TINYINT(4), nullable=False, server_default=FetchedValue())
    deaths = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    total_renown = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    quests_completed = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    challenges_completed = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    game_type = Column(TINYINT(4), nullable=False, server_default=FetchedValue())

    player_class = relationship('PlayerClass')
    player_race = relationship('PlayerRace')

    @cached_property
    def birth_dt(self):
        """Datetime of player birth"""
        return datetime.datetime.fromtimestamp(self.birth)

    @cached_property
    def birth_ago(self):
        """Stringified approximate timedelta since player birth"""
        return delta.stringify(datetime.datetime.utcnow() - self.birth_dt)

    @cached_property
    def logon_dt(self):
        """Datetime of last player log on"""
        return datetime.datetime.fromtimestamp(self.logon)

    @cached_property
    def logon_ago(self):
        """Stringified approximate timedelta since player log on"""
        return delta.stringify(datetime.datetime.utcnow() - self.logon_dt)

    @cached_property
    def logout_dt(self):
        """Datetime of last player log out"""
        return datetime.datetime.fromtimestamp(self.logout)

    @cached_property
    def logout_ago(self):
        """Stringified approximate timedelta since player log out"""
        return delta.stringify(datetime.datetime.utcnow() - self.logout_dt)

    @cached_property
    def online_delta(self):
        """Timedelta of player total online time"""
        return datetime.timedelta(seconds=self.online)

    @cached_property
    def online_time(self):
        """Stringified approximate timedelta of player total online time"""
        return delta.stringify(self.online_delta)

    @cached_property
    def is_god(self):
        """Boolean whether player is a God"""
        if self.true_level >= max(IMM_LEVELS):
            return True
        return False

    @cached_property
    def is_immortal(self):
        """Boolean whether player is an immortal"""
        if self.true_level >= min(IMM_LEVELS):
            return True
        return False

    @cached_property
    def is_survival(self):
        """Boolean whether player is Survival (permdeath)"""
        if self.game_type == 1:
            return True
        return False

    @cached_property
    def player_alignment(self):
        """Player alignment"""
        for text, (low, high) in ALIGNMENTS.items():
            if self.align >= low and self.align <= high:
                return text
        return 'Unknown'

    @cached_property
    def player_css(self):
        """Player CSS class"""
        return f'{self.player_type}'.lower() + '-player'

    @cached_property
    def player_link(self):
        """Player link"""
        player_url = url_for('players.view', player_name=self.name, _anchor='player')
        return f'<a href="{player_url}">{self.name}</a>'

    @cached_property
    def player_title(self):
        """Player title"""
        return self.title.replace('%s', self.player_link)

    @cached_property
    def player_type(self):
        """Player type - returns string, one of:
            an immortal description (one of mud_secret.IMM_LEVELS), or
            Dead, Survival, or Classic"""
        if self.is_immortal:
            return IMM_LEVELS[self.true_level]
        if self.is_deleted == 1:
            return 'Dead'
        if self.is_survival:
            return 'Survival'
        return 'Classic'

    @property
    def seasonal_earned(self):
        """Amount of essence earned for the player"""

        # Immortal players do not earn essence
        if self.is_immortal:
            return 0

        # Survival players earn less essence from renown
        divisor = 10
        if self.is_survival:
            divisor = 20

        # Start with two (2) points for existing, with renown/remort equation
        earned = int(self.total_renown / divisor) + 2
        if self.remorts > 0:
            earned += int(self.remorts / 5) * 3 + 1
        return earned
