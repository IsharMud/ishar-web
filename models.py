"""Database classes/models"""
from datetime import datetime, timedelta
from functools import cached_property

from flask import url_for
from flask_login import current_user, UserMixin
from passlib.hash import md5_crypt

from sqlalchemy import Column, ForeignKey, Index, String, Table, TIMESTAMP, \
    Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import backref, relationship

from config import ALIGNMENTS, IMM_LEVELS, MUD_PODIR
from delta import stringify
from database import Base, db_session, metadata


class Account(Base, UserMixin):
    """Account used to log in to the website and MUD in-game"""
    __tablename__ = 'accounts'

    account_id = Column(INTEGER(11), primary_key=True)
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()")
    )
    seasonal_points = Column(
        MEDIUMINT(4), nullable=False, server_default=text("0")
    )
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(36), nullable=False)
    create_isp = Column(String(25), nullable=False)
    last_isp = Column(String(25), nullable=False)
    create_ident = Column(String(25), nullable=False)
    last_ident = Column(String(25), nullable=False)
    create_haddr = Column(INTEGER(11), nullable=False)
    last_haddr = Column(INTEGER(11), nullable=False)
    account_name = Column(String(25), nullable=False, unique=True)
    account_gift = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("'0000-00-00 00:00:00'")
    )

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


class AccountUpgrade(Base):
    """Upgrades that are available to accounts"""
    __tablename__ = 'account_upgrades'

    id = Column(TINYINT(4), primary_key=True)
    cost = Column(MEDIUMINT(4), nullable=False)
    description = Column(String(200), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    max_value = Column(MEDIUMINT(4), nullable=False, server_default=text("1"))
    scale = Column(TINYINT(4), nullable=False, server_default=text("1"))
    is_disabled = Column(TINYINT(1), nullable=False, server_default=text("0"))

    def __repr__(self):
        return (f'<AccountUpgrade> "{self.name}" ({self.id}) / '
                f'Cost: {self.cost} / Max: {self.max_value}')


class AccountsUpgrade(Base):
    """Account upgrade associated with account, and the level of upgrade"""
    __tablename__ = 'accounts_account_upgrades'

    account_upgrades_id = Column(
        ForeignKey(
            'account_upgrades.id',
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    account_id = Column(
        ForeignKey(
            'accounts.account_id',
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    amount = Column(MEDIUMINT(4), nullable=False)

    account = relationship('Account', backref='upgrades')
    upgrade = relationship('AccountUpgrade')

    def __repr__(self):
        return (f'<AccountsUpgrade> {self.upgrade} : {self.amount} @ '
                f'{self.account}')


class Challenge(Base):
    """Challenge mobiles available for players to kill in-game for rewards"""
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
    winner_desc = Column(
        String(80),
        nullable=False,
        server_default=text("'--'")
    )
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
        return (f'{tiers[self.adj_tier]} ({tiers[self.orig_tier]})')

    def __repr__(self):
        return (f'<Challenge> "{self.mob_name}" ({self.challenge_id}) / '
                f'Active: {self.is_active} / Tier: "{self.display_tier}" / '
                f'Winner: "{self.winner_desc}"')


class GlobalEvent(Base):
    """Global events within the game, which provide bonuses"""
    __tablename__ = 'global_event'

    event_type = Column(TINYINT(4), primary_key=True, unique=True)
    start_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            "current_timestamp() ON UPDATE current_timestamp()"
        )
    )
    end_time = Column(
        TIMESTAMP, nullable=False,
        server_default=text("'0000-00-00 00:00:00'")
    )
    event_name = Column(String(20), nullable=False)
    event_desc = Column(String(40), nullable=False)
    xp_bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    shop_bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    celestial_luck = Column(
        TINYINT(1),
        nullable=False,
        server_default=text("0")
    )

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
        return ('<GlobalEvent> / '
                f'Type: "{self.event_type}" / '
                f'Name: "{self.event_name}" ("{self.display_name}") / '
                f'Desc: "{self.event_desc}" / '
                f'Start: "{self.start_time}" ("{self.start}") / '
                f'End: "{self.end_time}" ("{self.end}")')


class News(Base):
    """News posts for the front page of the website"""
    __tablename__ = 'news'

    news_id = Column(INTEGER(11), primary_key=True)
    account_id = Column(
        ForeignKey(
            'accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'
        ), nullable=False, index=True
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            "current_timestamp() ON UPDATE current_timestamp()"
        )
    )
    subject = Column(String(64), nullable=False, server_default=text("''"))
    body = Column(Text, nullable=False)

    account = relationship('Account')

    def __repr__(self):
        return (f'<News> "{self.subject}" ({self.news_id}) @ '
                f'{self.created_at} by {self.account}')


class Class(Base):
    """Classes available when creating a player character:
        such as Cleric, Magician, Warrior, etc."""
    __tablename__ = 'classes'

    class_id = Column(TINYINT(3), primary_key=True)
    class_name = Column(
        String(15),
        nullable=False,
        unique=True,
        server_default=text("'NO_CLASS'")
    )
    class_display = Column(String(32))
    class_description = Column(String(64))

    @cached_property
    def class_display_name(self):
        """Human-readable display name for a player class"""
        return self.class_name.replace('_', '-').title()

    @cached_property
    def stats_order(self):
        """Order which stats should be in, based upon player class"""

        if self.class_name == 'WARRIOR':
            return ['Strength', 'Agility', 'Endurance',
                    'Willpower', 'Focus', 'Perception']
        if self.class_name == 'ROGUE':
            return ['Agility', 'Perception', 'Strength',
                    'Focus', 'Endurance', 'Willpower']
        if self.class_name == 'CLERIC':
            return ['Willpower', 'Strength', 'Perception',
                    'Endurance', 'Focus', 'Agility']
        if self.class_name == 'MAGICIAN':
            return ['Perception', 'Focus', 'Agility',
                    'Willpower', 'Endurance', 'Strength']
        if self.class_name == 'NECROMANCER':
            return ['Focus', 'Willpower', 'Perception',
                    'Agility', 'Strength', 'Endurance']

        # Alphabetic as last resort
        return ['Agility', 'Endurance', 'Focus',
                'Perception', 'Strength', 'Willpower']

    def __repr__(self):
        return (f'<Class> "{self.class_name}" ({self.class_id})')


class PlayerCommon(Base):
    """Common data of players that is shared with in-game 'mobiles'"""
    __tablename__ = 'player_common'

    player_id = Column(
        ForeignKey(
            'players.id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    class_id = Column(
        ForeignKey(
            'classes.class_id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    race_id = Column(
        ForeignKey(
            'races.race_id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    sex = Column(TINYINT(4), nullable=False, server_default=text("0"))
    level = Column(TINYINT(3), nullable=False)
    weight = Column(SMALLINT(5), nullable=False)
    height = Column(SMALLINT(5), nullable=False)
    comm_points = Column(SMALLINT(6), nullable=False)
    alignment = Column(SMALLINT(6), nullable=False)
    strength = Column(TINYINT(3), nullable=False)
    agility = Column(TINYINT(3), nullable=False)
    endurance = Column(TINYINT(3), nullable=False)
    perception = Column(TINYINT(3), nullable=False)
    focus = Column(TINYINT(3), nullable=False)
    willpower = Column(TINYINT(3), nullable=False)
    init_strength = Column(TINYINT(3), nullable=False)
    init_agility = Column(TINYINT(3), nullable=False)
    init_endurance = Column(TINYINT(3), nullable=False)
    init_perception = Column(TINYINT(3), nullable=False)
    init_focus = Column(TINYINT(3), nullable=False)
    init_willpower = Column(TINYINT(3), nullable=False)
    perm_hit_pts = Column(SMALLINT(6), nullable=False)
    perm_move_pts = Column(SMALLINT(6), nullable=False)
    perm_spell_pts = Column(SMALLINT(6), nullable=False)
    perm_favor_pts = Column(SMALLINT(6), nullable=False)
    curr_hit_pts = Column(SMALLINT(6), nullable=False)
    curr_move_pts = Column(SMALLINT(6), nullable=False)
    curr_spell_pts = Column(SMALLINT(6), nullable=False)
    curr_favor_pts = Column(SMALLINT(6), nullable=False)
    experience = Column(INTEGER(11), nullable=False)
    gold = Column(MEDIUMINT(9), nullable=False)
    karma = Column(MEDIUMINT(9), nullable=False)

    player = relationship(
        'Player',
        backref=backref(
            'common',
            cascade='all, delete-orphan',
            uselist=False
        )
    )
    player_class = relationship('Class')
    player_race = relationship('Race')

    def __repr__(self):
        return (f'<PlayerCommon> {self.player} / {self.player_class} / '
                f'{self.player_race}')


class Player(Base):
    """Player characters"""
    __tablename__ = 'players'

    id = Column(INTEGER(11), primary_key=True)
    account_id = Column(
        ForeignKey(
            'accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        nullable=False,
        index=True
    )
    name = Column(
        String(15),
        nullable=False,
        unique=True,
        server_default=text("''")
    )
    create_ident = Column(
        String(10),
        nullable=False,
        server_default=text("''")
    )
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
    is_deleted = Column(
        TINYINT(4),
        nullable=False,
        server_default=text("0")
    )
    deaths = Column(
        SMALLINT(5),
        nullable=False,
        server_default=text("0")
    )
    total_renown = Column(
        SMALLINT(5), nullable=False, server_default=text("0")
    )
    quests_completed = Column(
        SMALLINT(5), nullable=False, server_default=text("0")
    )
    challenges_completed = Column(
        SMALLINT(5), nullable=False, server_default=text("0")
    )
    game_type = Column(TINYINT(4), nullable=False, server_default=text("0"))
    birth = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("'0000-00-00 00:00:00'")
    )
    logon = Column(
        TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'")
    )
    logout = Column(
        TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'")
    )

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
        return self.is_immortal_type(immortal_type='God')

    @cached_property
    def is_artisan(self):
        """Boolean whether player is an Artisan (or above)"""
        return self.is_immortal_type(immortal_type='Artisan')

    @cached_property
    def is_consort(self):
        """Boolean whether player is a Consort (or above)"""
        return self.is_immortal_type(immortal_type='Consort')

    @cached_property
    def is_eternal(self):
        """Boolean whether player is an Eternal (or above)"""
        return self.is_immortal_type(immortal_type='Eternal')

    @cached_property
    def is_forger(self):
        """Boolean whether player is a Forger (or above)"""
        return self.is_immortal_type(immortal_type='Forger')

    @cached_property
    def is_immortal(self):
        """Boolean whether player is immortal (or above, but not consort)"""
        return self.is_immortal_type(immortal_type='Immortal')

    @cached_property
    def immortal_type(self):
        """Immortal type"""
        if self.true_level in IMM_LEVELS.keys():
            return IMM_LEVELS[self.true_level]
        return None

    def is_immortal_type(self, immortal_type='Immortal'):
        """Boolean whether player is a specific immortal type (or above)"""
        IMM_TYPES = {imm_type: level for level, imm_type in IMM_LEVELS.items()}
        if self.immortal_type:
            if self.immortal_type in IMM_TYPES.keys():
                if self.true_level >= IMM_TYPES[immortal_type]:
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
        for align_text, (low, high) in ALIGNMENTS.items():
            if low <= self.common.alignment <= high:
                return align_text
        return 'Unknown'

    @cached_property
    def player_css(self):
        """Player CSS class"""
        return (f'{self.player_type.lower()}-player')

    @cached_property
    def player_stats(self):
        """Player stats"""

        # Start with an empty dictionary for the players stats
        stats = {}

        # Gods can always see player's stats
        if not current_user.is_god:

            # Return the empty dictionary, meaning no visible stats, for:

            # - Immortal players, and...
            if self.is_immortal:
                return stats

            # - Mortal players below level five (5),
            #       with less than one (1) hour of play-time
            if self.true_level < 5 and self.online < 3600:
                return stats

        # Get the players stats
        players_stats = {
            'Agility': self.common.agility,
            'Endurance': self.common.endurance,
            'Focus': self.common.focus,
            'Perception': self.common.perception,
            'Strength': self.common.strength,
            'Willpower': self.common.willpower
        }

        # Put the players stats in the appropriate order,
        #   based on their class, and return them
        for stat_order in self.common.player_class.stats_order:
            stats[stat_order] = players_stats[stat_order]
        return stats

    @cached_property
    def player_link(self):
        """Player link"""
        url = url_for(
            'portal.view_player',
            player_name=self.name,
            _anchor='player'
        )
        return (f'<a href="{url}">{self.name}</a>')

    @cached_property
    def player_title(self):
        """Player title"""
        return self.title.replace('%s', self.player_link)

    @cached_property
    def player_type(self):
        """
        Player type (string), returns one of:
            - An immortal type
                * one of config.IMM_LEVELS dictionary values
            - Dead, Survival, or Classic
        """
        if self.immortal_type:
            return self.immortal_type
        if self.is_deleted == 1:
            return 'Dead'
        if self.is_survival:
            return 'Survival'
        return 'Classic'

    @cached_property
    def podir(self):
        """Player podir"""
        return (f'{MUD_PODIR}/{self.name}')

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

    def __repr__(self):
        return (f'<Player> "{self.name}" ({self.id}) / '
                f'Type: {self.player_type} / True Level: {self.true_level}')


class PlayerRemortUpgrade(Base):
    """Remort upgrades that player characters have"""
    __tablename__ = 'player_remort_upgrades'

    upgrade_id = Column(
        ForeignKey(
            'remort_upgrades.upgrade_id',
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    player_id = Column(
        ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
        index=True
    )
    value = Column(INTEGER(11), nullable=False)
    essence_perk = Column(
        TINYINT(1), nullable=False, server_default=text("0")
    )

    player = relationship('Player', backref='remort_upgrades')
    remort_upgrade = relationship('RemortUpgrade')

    def __repr__(self):
        return (f'<PlayerRemortUpgrade> "{self.remort_upgrade}" '
                f'({self.upgrade_id}) : {self.value} ({self.essence_perk}) @ '
                f'{self.player}')


# Associate quests with pre-reqs
t_quest_prereqs = Table(
    'quest_prereqs', metadata,
    Column(
        'quest_id',
        ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True
    ),
    Column(
        'required_quest',
        ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True
    )
)


class PlayerQuest(Base):
    """Associate players with quests"""
    __tablename__ = 'player_quests'
    __table_args__ = (
        Index('quest_id', 'quest_id', 'player_id', unique=True),
    )

    quest_id = Column(
        ForeignKey(
            'quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    player_id = Column(
        ForeignKey(
            'players.id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    status = Column(TINYINT(11), nullable=False)
    last_completed_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            "current_timestamp() ON UPDATE current_timestamp()"
        )
    )
    num_completed = Column(
        TINYINT(4),
        nullable=False,
        server_default=text("0")
    )

    player = relationship('Player')
    quest = relationship('Quest')

    def __repr__(self):
        return (f'<PlayerQuest> {self.player} @ {self.quest}')


class PlayerQuestStep(Base):
    """Steps of a players quest"""
    __tablename__ = 'player_quest_steps'

    player_id = Column(
        ForeignKey(
            'players.id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    step_id = Column(
        ForeignKey(
            'quest_steps.step_id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    num_collected = Column(TINYINT(1), nullable=False)

    player = relationship('Player')
    step = relationship('QuestStep')

    def __repr__(self):
        return (f'<PlayerQuestStep> {self.player} @ {self.step} : '
                f'{self.num_collected}')


class Quest(Base):
    """Quest available to players"""
    __tablename__ = 'quests'

    quest_id = Column(INTEGER(11), primary_key=True)
    name = Column(
        String(25),
        nullable=False,
        unique=True,
        server_default=text("''")
    )
    display_name = Column(String(30), nullable=False)
    completion_message = Column(String(80), nullable=False)
    min_level = Column(TINYINT(4), nullable=False, server_default=text("1"))
    max_level = Column(TINYINT(4), nullable=False, server_default=text("20"))
    repeatable = Column(TINYINT(1), nullable=False, server_default=text("0"))
    description = Column(
        String(512),
        nullable=False,
        server_default=text("'No description available.'")
    )
    prerequisite = Column(
        INTEGER(11), nullable=False, server_default=text("-1")
    )
    # class_restrict = Column(
    #     TINYINT(4),
    #     nullable=False,
    #     server_default=text("-1")
    # )
    class_restrict = Column(
        ForeignKey(
            'classes.class_id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False,
        index=True
    )
    quest_intro = Column(
        String(1600), nullable=False, server_default=text("''")
    )

    parents = relationship(
        'Quest',
        secondary='quest_prereqs',
        primaryjoin='Quest.quest_id == quest_prereqs.c.quest_id',
        secondaryjoin='Quest.quest_id == quest_prereqs.c.required_quest'
    )

    restricted_class = relationship('Class')

    def __repr__(self):
        return (f'<Quest> "{self.name}" ({self.quest_id}) / '
                f'Levels: {self.min_level} - {self.max_level} / '
                f'Parents: {self.parents} / Class: {self.restricted_class}')


class QuestReward(Base):
    """Rewards for completion of a quest"""
    __tablename__ = 'quest_rewards'

    reward_num = Column(INTEGER(11), primary_key=True, nullable=False)
    reward_type = Column(TINYINT(2), nullable=False)
    quest_id = Column(
        ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
        index=True
    )

    quest = relationship('Quest')

    def __repr__(self):
        return (f'<QuestReward> "{self.reward_num}" ({self.reward_type}) @ '
                f'{self.quest}')


class QuestStep(Base):
    """Steps of a quest"""
    __tablename__ = 'quest_steps'

    step_id = Column(TINYINT(4), primary_key=True)
    step_type = Column(TINYINT(4), nullable=False)
    target = Column(INTEGER(11), nullable=False)
    num_required = Column(INTEGER(11), nullable=False)
    quest_id = Column(
        ForeignKey(
            'quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        nullable=False,
        index=True
    )
    time_limit = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    mystify = Column(TINYINT(1), nullable=False, server_default=text("0"))
    mystify_text = Column(
        String(80), nullable=False, server_default=text("''")
    )

    quest = relationship('Quest')

    def __repr__(self):
        return (f'<QuestStep> "{self.step_type}" ({self.step_id}) @ '
                f'{self.quest})')


class Race(Base):
    """Races available when creating a player character:
        such as Elf, Gnome, Human, etc., and their attributes"""
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
    is_invertebrae = Column(
        TINYINT(1), nullable=False, server_default=text("0")
    )
    is_flying = Column(TINYINT(1), nullable=False, server_default=text("0"))
    is_swimming = Column(TINYINT(1), nullable=False, server_default=text("0"))
    darkvision = Column(TINYINT(4), nullable=False, server_default=text("0"))
    see_invis = Column(TINYINT(1), nullable=False, server_default=text("0"))
    is_walking = Column(TINYINT(1), nullable=False, server_default=text("1"))
    endure_heat = Column(TINYINT(1), nullable=False, server_default=text("0"))
    endure_cold = Column(TINYINT(1), nullable=False, server_default=text("0"))
    is_undead = Column(TINYINT(1), nullable=False, server_default=text("0"))

    def __repr__(self):
        return (f'<Race> "{self.display_name}" ({self.symbol} : '
                f'({self.race_id})')


class RemortUpgrade(Base):
    """Remort upgrades that are available to player characters"""
    __tablename__ = 'remort_upgrades'

    upgrade_id = Column(INTEGER(11), primary_key=True)
    name = Column(
        String(20), nullable=False, unique=True, server_default=text("''")
    )
    renown_cost = Column(SMALLINT(6), nullable=False)
    max_value = Column(SMALLINT(6), nullable=False)
    scale = Column(TINYINT(4), nullable=False, server_default=text("10"))
    display_name = Column(String(30), nullable=False)
    can_buy = Column(TINYINT(1), nullable=False, server_default=text("1"))
    bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    survival_scale = Column(TINYINT(4), nullable=False)
    survival_renown_cost = Column(TINYINT(4), nullable=False)

    def __repr__(self):
        return (f'<RemortUpgrade> "{self.display_name}" ({self.upgrade_id})')


class Season(Base):
    """Details of the start and end times of in-game cyclical seasons"""
    __tablename__ = 'seasons'

    season_id = Column(INTEGER(11), primary_key=True)
    is_active = Column(TINYINT(4), nullable=False)
    effective_date = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            "current_timestamp() ON UPDATE current_timestamp()"
        )
    )
    expiration_date = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            "'0000-00-00 00:00:00'"
        )
    )

    @property
    def effective(self):
        """Stringified approximate timedelta since season started"""
        return stringify(datetime.utcnow() - self.effective_date)

    @property
    def expires(self):
        """Stringified approximate timedelta until season ends"""
        return stringify(self.expiration_date - datetime.utcnow())

    def __repr__(self):
        return (f'<Season> {self.season_id} / Active: {self.is_active} / '
                f'{self.effective_date} ({self.effective}) - '
                f'{self.expiration_date} ({self.expires})')
