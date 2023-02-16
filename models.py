"""Database classes/models"""
from datetime import datetime, timedelta
from functools import cached_property

from flask import url_for
from flask_login import current_user, UserMixin
from passlib.hash import md5_crypt

from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship

from mud_secret import ALIGNMENTS, IMM_LEVELS, PODIR
from delta import stringify
from database import Base, db_session, metadata


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

    def __str__(self):
        return f'<Account> "{self.display_name}" (ID: {self.account_id})'

    def __repr__(self):
        return f'<Account> "{self.account_name}" (ID: {self.account_id})'


class AccountUpgrade(Base):
    """Account upgrades that are available to accounts"""
    __tablename__ = 'account_upgrades'

    id = Column(TINYINT(4), primary_key=True)
    cost = Column(MEDIUMINT(4), nullable=False)
    description = Column(String(200), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    max_value = Column(MEDIUMINT(4), nullable=False, server_default=text("1"))
    scale = Column(TINYINT(4), nullable=False, server_default=text("1"))
    is_disabled = Column(TINYINT(1), nullable=False, server_default=text("0"))

    def __repr__(self):
        return f'<AccountUpgrade> "{self.name}" ({self.id}) / ' \
               f'Cost: {self.cost} / Max Value: {self.max_value}'


class AccountsUpgrade(Base):
    """Account upgrade associated with account, and the level of upgrade"""
    __tablename__ = 'accounts_account_upgrades'

    account_upgrades_id = Column(ForeignKey('account_upgrades.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    amount = Column(MEDIUMINT(4), nullable=False)

    account = relationship('Account')
    upgrade = relationship('AccountUpgrade')

    def __repr__(self):
        return f'<AccountsUpgrade> "{self.upgrade.name}" ' \
               f'({self.account_upgrades_id}) @ ' \
               f'<Account> "{self.account.account_name}" ({self.account_id})' \
               f' / Amount: {self.amount}'


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

    @cached_property
    def is_completed(self):
        """Boolean whether challenge is completed"""
        if self.winner_desc != '' and self.winner_desc != "'--'":
            return True
        return False

    @cached_property
    def display_tier(self):
        """Display challenge tier"""
        tiers = {
            1: 'F', 2: 'D', 3: 'C',
            4: 'B', 5: 'A', 6: 'S',
            7: 'SS', 8: 'SS', 9: 'SS'
        }
        return f'{tiers[self.adj_tier]} ({tiers[self.orig_tier]})'

    def __repr__(self):
        return f'<Challenge> "{self.mob_name}" ({self.challenge_id}) / ' \
               f'Active: {self.is_active} / Tier: "{self.display_tier}" / ' \
               f'winner_desc: "{self.winner_desc}"'


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

    @property
    def start(self):
        """Stringified approximate timedelta since event start"""
        return stringify(datetime.utcnow() - self.start_time)

    @property
    def end(self):
        """Stringified approximate timedelta until event end"""
        return stringify(self.end_time - datetime.utcnow())

    @cached_property
    def display_name(self):
        """Formatted name of the event"""
        return self.event_name.replace('_', ' ').title()

    @cached_property
    def display_string(self):
        """Formatted full display string for the event,
            with display name, and any event_desc from database"""
        out = self.display_name
        if self.event_desc and self.event_desc != '':
            out += f' -- {self.event_desc}'
        return out

    @cached_property
    def is_luck(self):
        """Boolean based upon celestial_luck from database"""
        if self.celestial_luck == 1:
            return True
        return False

    def __repr__(self):
        return '<GlobalEvent> / ' \
               f'Type: "{self.event_type}" / ' \
               f'Name: "{self.event_name}" ("{self.display_name}") / ' \
               f'Desc: "{self.event_desc}" / ' \
               f'Start: "{self.start_time}" ("{self.start}") / ' \
               f'End: "{self.end_time}" ("{self.end}")'


class News(Base):
    __tablename__ = 'news'

    news_id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    subject = Column(String(64), nullable=False, server_default=text("''"))
    body = Column(Text, nullable=False)

    account = relationship('Account')

    def __repr__(self):
        return f'<News> "{self.subject}" ({self.news_id}) @ ' \
               f'"{self.created_at}"'


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

    account = relationship('Account', backref='players')

    @cached_property
    def birth_ago(self):
        """Stringified approximate timedelta since player birth"""
        return stringify(datetime.utcnow() - self.birth)

    @cached_property
    def logon_ago(self):
        """Stringified approximate timedelta since player log on"""
        return stringify(datetime.utcnow() - self.logon)

    @cached_property
    def logout_ago(self):
        """Stringified approximate timedelta since player log out"""
        return stringify(datetime.utcnow() - self.logout)

    @cached_property
    def online_delta(self):
        """Timedelta of player total online time"""
        return timedelta(seconds=self.online)

    @cached_property
    def online_time(self):
        """Stringified approximate timedelta of player total online time"""
        return stringify(self.online_delta)

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
            if low <= self.align <= high:
                return text
        return 'Unknown'

    @cached_property
    def player_css(self):
        """Player CSS class"""
        return f'{self.player_type}'.lower() + '-player'

    @cached_property
    def player_stats(self):
        """Player stats"""

        # Start with an empty dictionary for the players stats
        stats = {}

        # Gods can always see player's stats
        if not current_user.is_god:

            # Return the empty dictionary, meaning no visible stats, for:

            #   - Immortal players, and...
            if self.is_immortal:
                return stats

            #   - Mortal players below level five (5), with less than one (1) hour of play-time
            if self.true_level < 5 and self.online < 3600:
                return stats

        # Get the players stats
        players_stats = {
            'Agility': self.curr_agility, 'Endurance': self.curr_endurance,
            'Focus': self.curr_focus, 'Perception': self.curr_perception,
            'Strength': self.curr_strength, 'Willpower': self.curr_willpower
        }

        # Put the players stats in the appropriate order,
        #   based on their class, and return them
        for stat_order in self.player_class.stats_order:
            stats[stat_order] = players_stats[stat_order]
        return stats

    @cached_property
    def player_link(self):
        """Player link"""
        url = url_for('portal.view_player', player_name=self.name, _anchor='player')
        return f'<a href="{url}">{self.name}</a>'

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

    @cached_property
    def podir(self):
        """Player Podir"""
        return f'{PODIR}/{self.name}'

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

        # Start with two (2) points for existing,
        #   with renown/remort equation
        earned = int(self.total_renown / divisor) + 2
        if self.remorts > 0:
            earned += int(self.remorts / 5) * 3 + 1
        return earned


class PlayerClass(Base):
    __tablename__ = 'classes'

    class_id = Column(TINYINT(3), primary_key=True)
    class_name = Column(String(15), nullable=False, unique=True, server_default=text("'NO_CLASS'"))
    class_display = Column(String(32))
    class_description = Column(String(64))

    player_class = relationship('Player', secondary='player_common', backref='player_class')

    @cached_property
    def class_display_name(self):
        """Human-readable display name for a player class"""
        return self.class_name.replace('_', '-').title()

    @cached_property
    def stats_order(self):
        """Order which stats should be in, based upon player class"""
        if self.class_name == 'WARRIOR':
            return ['Strength', 'Agility', 'Endurance', 'Willpower', 'Focus', 'Perception']
        if self.class_name == 'ROGUE':
            return ['Agility', 'Perception', 'Strength', 'Focus', 'Endurance', 'Willpower']
        if self.class_name == 'CLERIC':
            return ['Willpower', 'Strength', 'Perception', 'Endurance', 'Focus', 'Agility']
        if self.class_name == 'MAGICIAN':
            return ['Perception', 'Focus', 'Agility', 'Willpower', 'Endurance', 'Strength']
        if self.class_name == 'NECROMANCER':
            return ['Focus', 'Willpower', 'Perception', 'Agility', 'Strength', 'Endurance']
        # Alphabetic as a last resort
        return ['Agility', 'Endurance', 'Focus', 'Perception', 'Strength', 'Willpower']

    def __repr__(self):
        return f'<PlayerClass> "{self.class_name}" ({self.class_id})'


class PlayerRace(Base):
    __tablename__ = 'races'

    race_id = Column(TINYINT(3), primary_key=True)
    race_name = Column(String(15), nullable=False, unique=True)
    race_description = Column(String(64))

    player_race = relationship('Player', secondary='player_common', backref='player_race')

    @cached_property
    def race_display_name(self):
        """Human-readable display name for a player race"""
        return self.race_name.replace('_', '-').title()

    def __repr__(self):
        return f'<PlayerRace> "{self.race_name}" ({self.race_id})'


class PlayerRemortUpgrade(Base):
    __tablename__ = 'player_remort_upgrades'

    upgrade_id = Column(ForeignKey('remort_upgrades.upgrade_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(INTEGER(11), nullable=False)
    essence_perk = Column(TINYINT(1), nullable=False, server_default=text("0"))

    player = relationship('Player', backref='remort_upgrades')
    remort_upgrade = relationship('RemortUpgrade')


    def __repr__(self):
        return f'<PlayerRemortUpgrade> "{self.remort_upgrade.name}" ' \
               f'({self.upgrade_id}) @ <Player> "{self.player.name}" ' \
               f'({self.player_id}) / Value: {self.value}'


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

    def __repr__(self):
        return f'<RemortUpgrade> "{self.name}" ({self.upgrade_id}) / ' \
               f'Cost: {self.renown_cost} / Max: {self.max_value}'


class Season(Base):
    __tablename__ = 'seasons'

    season_id = Column(INTEGER(11), primary_key=True)
    is_active = Column(TINYINT(4), nullable=False)
    effective_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    expiration_date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))

    @property
    def effective(self):
        """Stringified approximate timedelta since season started"""
        return stringify(datetime.utcnow() - self.effective_date)

    @property
    def expires(self):
        """Stringified approximate timedelta until season ends"""
        return stringify(self.expiration_date - datetime.utcnow())

    def __repr__(self):
        return f'<Season> ID {self.season_id} / Active: {self.is_active} / ' \
               f'Effective: {self.effective_date} ("{self.effective}") - ' \
               f'Expires: {self.expiration_date} ("{self.expires}")'


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
