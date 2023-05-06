"""Database classes/models"""
from datetime import datetime, timedelta

from flask import url_for
from flask_login import current_user

from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT
from sqlalchemy.orm import relationship

from config import ALIGNMENTS, IMM_LEVELS, MUD_PODIR
from delta import stringify
from database import Base, metadata
from .quest import PlayerQuest
from .upgrade import PlayerRemortUpgrade


class Player(Base):
    """Player characters"""
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

    account = relationship(
        'Account',
        back_populates='players',
        single_parent=True,
        uselist=False
    )

    common = relationship(
        'PlayerCommon',
        single_parent=True,
        uselist=False
    )

    quests = relationship(
        'PlayerQuest',
        single_parent=True,
        uselist=True
    )

    remort_upgrades = relationship(
        'PlayerRemortUpgrade',
        single_parent=True,
        uselist=True
    )

    @property
    def birth_ago(self):
        """Stringified approximate timedelta since player birth"""
        return stringify(datetime.utcnow() - self.birth)

    @property
    def logon_ago(self):
        """Stringified approximate timedelta since player log on"""
        return stringify(datetime.utcnow() - self.logon)

    @property
    def logout_ago(self):
        """Stringified approximate timedelta since player log out"""
        return stringify(datetime.utcnow() - self.logout)

    @property
    def online_delta(self):
        """Timedelta of player total online time"""
        return timedelta(seconds=self.online)

    @property
    def online_time(self):
        """Stringified approximate timedelta of player total online time"""
        return stringify(self.online_delta)

    @property
    def is_god(self):
        """Boolean whether player is a God"""
        return self.is_immortal_type(immortal_type='God')

    @property
    def is_artisan(self):
        """Boolean whether player is an Artisan (or above)"""
        return self.is_immortal_type(immortal_type='Artisan')

    @property
    def is_consort(self):
        """Boolean whether player is a Consort (or above)"""
        return self.is_immortal_type(immortal_type='Consort')

    @property
    def is_eternal(self):
        """Boolean whether player is an Eternal (or above)"""
        return self.is_immortal_type(immortal_type='Eternal')

    @property
    def is_forger(self):
        """Boolean whether player is a Forger (or above)"""
        return self.is_immortal_type(immortal_type='Forger')

    @property
    def is_immortal(self):
        """Boolean whether player is immortal (or above, but not consort)"""
        return self.is_immortal_type(immortal_type='Immortal')

    @property
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

    @property
    def is_survival(self):
        """Boolean whether player is Survival (permdeath)"""
        if self.game_type == 1:
            return True
        return False

    @property
    def player_alignment(self):
        """Player alignment"""
        for align_text, (low, high) in ALIGNMENTS.items():
            if low <= self.common.alignment <= high:
                return align_text
        return 'Unknown'

    @property
    def player_css(self):
        """Player CSS class"""
        return (f'{self.player_type.lower()}-player')

    @property
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

    @property
    def player_link(self):
        """Player link"""
        url = url_for(
            'portal.view_player',
            player_name=self.name,
            _anchor='player'
        )
        return (f'<a href="{url}">{self.name}</a>')

    @property
    def player_title(self):
        """Player title"""
        return self.title.replace('%s', self.player_link)

    @property
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

    @property
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
                f'{self.player_type} [{self.true_level}]')
