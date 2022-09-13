import datetime
from flask import url_for
from flask_login import UserMixin
from passlib.hash import md5_crypt
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from database import Base, db_session
import delta
import levels

# Database classes/models


class Account(Base, UserMixin):
    """
    Account database class
    An account can have multiple players belonging to it
    Accounts exist to log-in in-game, and are also used on the website for flask-login/authentication, and registration
    "Seasonal points"/"essence" and "account upgrades" are per account, and can be spent any time (in-game, or on the website)
    However, "renown" and "remort upgrades" are per player - and these are only available to purchase in-game, at the "shrine"
    """
    __tablename__   = 'accounts'

    account_id      = Column(INTEGER(11), primary_key=True)
    created_at      = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    seasonal_points = Column(MEDIUMINT(4), nullable=False, server_default=FetchedValue())
    email           = Column(String(30), nullable=False, unique=True)
    password        = Column(String(36), nullable=False)
    create_isp      = Column(String(25), nullable=False)
    last_isp        = Column(String(25), nullable=False)
    create_ident    = Column(String(25), nullable=False)
    last_ident      = Column(String(25), nullable=False)
    create_haddr    = Column(INTEGER(11), nullable=False)
    last_haddr      = Column(INTEGER(11), nullable=False)
    account_name    = Column(String(25), nullable=False, unique=True)

    players         = relationship('Player', backref='account')

    def get_id(self):
        """flask-login method to return account ID"""
        return str(self.account_id)

    def is_active(self):
        """flask-login method to return boolean whether user is active"""
        return isinstance(self.account_id, int)

    def is_authenticated(self):
        """flask-login method to return boolean whether user is authenticated"""
        return isinstance(self.account_id, int)

    @hybrid_property
    def is_god(self):
        """Hybrid property returning boolean whether user is a "God" """
        for player in self.players:
            if player.is_god:
                return True
        return False

    @hybrid_property
    def seasonal_earned(self):
        """Hybrid property containing the amount of essence earned for the account"""

        # Start at zero (0), and return the points from the player within the account whom has earned the highest amount
        s = 0
        for player in self.players:
            if player.seasonal_earned > s:
                s = player.seasonal_earned
        return s

    def change_password(self, new_password):
        """Method to allow users to change their account password"""
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

    def create_account(self):
        """Method to create a new account"""
        try:

            # Hash the password and add the account to the database
            self.password = md5_crypt.hash(self.password)
            db_session.add(self)
            db_session.commit()

            # Start each available account upgrade at zero (0)
            for init_ugrade in AccountUpgrade.query.all():
                create_upgrade  = AccountsUpgrade(
                    account_upgrades_id     = init_ugrade.id,
                    account_id              = self.account_id,
                    amount                  = 0
                )
                db_session.add(create_upgrade)
            db_session.commit()

            # Return the new account ID
            return self.account_id

        except Exception as err:
            print(err)
        return False

    def __repr__(self):
        return f'<Account> "{self.account_name}" ({self.account_id})'


class AccountUpgrade(Base):
    """
    Account Upgrade database class
    Account upgrade available to accounts, as well as the essence cost and max value
    """
    __tablename__       = 'account_upgrades'

    id                  = Column(TINYINT(4), primary_key=True)
    cost                = Column(MEDIUMINT(4), nullable=False)
    description         = Column(String(200), nullable=False)
    name                = Column(String(30), nullable=False, unique=True)
    max_value           = Column(MEDIUMINT(4), nullable=False, server_default=FetchedValue())

    accounts_upgrade    = relationship('AccountsUpgrade', backref='upgrade')

    def __repr__(self):
        return f'<AccountUpgrade> "{self.name}" ({self.id}) / ' \
            f'Cost: {self.cost} / Max Value: {self.max_value}'


class AccountsUpgrade(Base):
    """
    Accounts Upgrade database class
    Account upgrade associated with account, and the level of upgrade
    """
    __tablename__       = 'accounts_account_upgrades'

    account_upgrades_id = Column(
                            ForeignKey('account_upgrades.id',
                                ondelete='CASCADE', onupdate='CASCADE'
                            ), nullable=False, index=True, primary_key=True
                        )
    account_id          = Column(
                            ForeignKey('accounts.account_id',
                                ondelete='CASCADE', onupdate='CASCADE'
                            ), nullable=False, index=True, primary_key=True
                        )
    amount              = Column(MEDIUMINT(4), nullable=False)

    account             = relationship('Account', backref='upgrades')

    def do_upgrade(self, increment=1):
        """Method to increment an account upgrade and reduce account seasonal points (essence)"""
        try:
            self.amount = self.amount + increment
            self.account.seasonal_points = self.account.seasonal_points - self.upgrade.cost
            db_session.commit()
            return True
        except Exception as err:
            print(err)
        return False

    def __repr__(self):
        return f'<AccountsUpgrade> "{self.upgrade.name}" ({self.account_upgrades_id}) @ <Account> "{self.account.account_name}" ({self.account_id}) / Amount: {self.amount}'


class Challenge(Base):
    """
    Challenge database class
    Challenge along with the in-game mobile ("mob")/target number (mob_vnum), as well as level/group requirements, and tier
    """
    __tablename__   = 'challenges'

    challenge_id    = Column(SMALLINT(4), primary_key=True)
    mob_vnum        = Column(INTEGER(11), nullable=False)
    orig_level      = Column(TINYINT(4), nullable=False)
    orig_people     = Column(TINYINT(4), nullable=False)
    orig_tier       = Column(TINYINT(4), nullable=False)
    adj_level       = Column(TINYINT(4), nullable=False)
    adj_people      = Column(TINYINT(4), nullable=False)
    adj_tier        = Column(TINYINT(4), nullable=False)
    challenge_desc  = Column(String(80), nullable=False)
    winner_desc     = Column(String(80), nullable=False, server_default=FetchedValue())
    mob_name        = Column(String(30), nullable=False)
    is_active       = Column(TINYINT(1), nullable=False, server_default=FetchedValue())

    @hybrid_property
    def is_completed(self):
        """Hybrid property returning boolean whether challenge is completed"""
        if self.winner_desc != '':
            return True
        return False

    @hybrid_property
    def reward_tier(self):
        """Hybrid property returning reward tier string"""
        tiers = { 9: 'SS', 8: 'SS', 7: 'SS', 6: 'S', 5: 'A', 4: 'B', 3: 'C', 2: 'D', 1: 'F' }
        if self.adj_tier in tiers.keys():
            return tiers[self.adj_tier]
        return self.adj_tier

    def __repr__(self):
        return f'<Challenge> "{self.mob_name}" ({self.challenge_id}) / ' \
            f'Active: {self.is_active} / Reward: "{self.reward_tier}" ' \
            f'({self.adj_tier}) / winner_desc: "{self.winner_desc}"'


class News(Base):
    """
    News database class
    News post for the main/welcome page
    """
    __tablename__   = 'news'

    news_id         = Column(INTEGER(11), primary_key=True)
    account_id      = Column(
                        ForeignKey('accounts.account_id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True
                    )
    created_at      = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    subject         = Column(String(64), nullable=False, server_default=FetchedValue())
    body            = Column(Text, nullable=False)

    account         = relationship('Account')

    def add_news(self):
        """Method to add a news post"""
        try:
            db_session.add(self)
            db_session.commit()
            return self.news_id
        except Exception as err:
            print(err)
        return False

    def __repr__(self):
        return f'<News> "{self.subject}" ({self.news_id}) / by "{self.account.name}" / at "{self.created_at}"'


class PlayerClass(Base):
    """
    Player Class database class
    Playable character "class" in-game such as warrior, magician, cleric, rogue, necromancer, etc.
    """
    __tablename__       = 'classes'

    class_id            = Column(TINYINT(3), primary_key=True)
    class_name          = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    class_display       = Column(String(32))
    class_description   = Column(String(64))

    player_class        = relationship('Player', backref='class')

    def __repr__(self):
        return f'<PlayerClass> "{self.class_name}" ({self.class_id})'


class PlayerFlag(Base):
    """
    Player Flag database class
    Flag for a setting affecting a player character in-game (such as perm-death/survival character, see is_survival)
    """
    __tablename__   = 'player_flags'

    flag_id         = Column(INTEGER(11), primary_key=True)
    name            = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<PlayerFlag> "{self.name}" ({self.flag_id})'


class PlayersFlag(Base):
    """
    Players Flag database class
    Flag associated with player and the flag value
    """
    __tablename__   = 'player_player_flags'

    flag_id         = Column(
                        ForeignKey('player_flags.flag_id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    value           = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    def __repr__(self):
        return f'<PlayersFlag> "{self.flag.name}" ({self.flag_id}) @ <Player> "{self.player.name}" ({self.player_id}) : {self.value}'


class PlayerRace(Base):
    """
    Player Race database class
    Playable character "race" in-game such as elf, gnome, human, etc.
    """
    __tablename__       = 'races'

    race_id             = Column(TINYINT(3), primary_key=True)
    race_name           = Column(String(15), nullable=False, unique=True)
    race_description    = Column(String(64))

    player_race         = relationship('Player', backref='race')

    def __repr__(self):
        return f'<PlayerRace> "{self.race_name}" ({self.race_id})'


class Quest(Base):
    """
    Quest database class
    Quest that can be achieved, and its rewards
    """
    __tablename__       = 'quests'

    quest_id            = Column(INTEGER(11), primary_key=True)
    name                = Column(String(25),
                            nullable=False, unique=True, server_default=FetchedValue())
    display_name        = Column(String(30), nullable=False)
    is_major            = Column(TINYINT(1), nullable=False, server_default=FetchedValue())
    xp_reward           = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    completion_message  = Column(String(80), nullable=False)

    def __repr__(self):
        return f'<Quest> "{self.name}" ({self.quest_id}) / ' \
            f'"{self.display_name}" / XP: {self.xp_reward}'


class PlayerQuest(Base):
    """
    Player Quest database class
    Quest associated with players completion
    """
    __tablename__   = 'player_quests'

    quest_id        = Column(
                        ForeignKey('quests.quest_id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    value           = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    quest           = relationship('Quest')
    player          = relationship('Player', backref='quests')

    def __repr__(self):
        return f'<PlayerQuest> "{self.quest.name}" ({self.quest_id}) @ ' \
            f'<Player> "{self.player.name}" ({self.player_id}) / Value: {self.value}'


class RemortUpgrade(Base):
    """
    Remort Upgrades database class
    Remort upgrade available to players, as well as the renown cost and max value
    """
    __tablename__   = 'remort_upgrades'

    upgrade_id      = Column(INTEGER(11), primary_key=True)
    name            = Column(String(20), nullable=False, unique=True, server_default=FetchedValue())
    renown_cost     = Column(SMALLINT(6), nullable=False)
    max_value       = Column(SMALLINT(6), nullable=False)

    remort_upgrades = relationship('PlayerRemortUpgrade', backref='remort_upgrade')

    def __repr__(self):
        return f'<RemortUpgrade> "{self.name}" ({self.upgrade_id}) / ' \
            f'Cost: {self.renown_cost} / Max: {self.max_value}'


class PlayerRemortUpgrade(Base):
    """
    Player Remort Upgrades database class
    Remort upgrade associated with player, and the level of upgrade
    """
    __tablename__   = 'player_remort_upgrades'

    upgrade_id      = Column(
                        ForeignKey('remort_upgrades.upgrade_id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    value           = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    player          = relationship('Player', backref='remort_upgrades')

    def __repr__(self):
        return f'<PlayerRemortUpgrade> "{self.remort_upgrade.name}" ' \
            f'({self.upgrade_id}) @ <Player> "{self.player.name}" ' \
            f'({self.player_id}) / Value: {self.value}'


class Season(Base):
    """
    Season database class
    In-game cyclical season detail and dates
    """
    __tablename__   = 'seasons'

    season_id       = Column(INTEGER(11), primary_key=True)
    is_active       = Column(TINYINT(4), nullable=False)
    effective_date  = Column(INTEGER(11), nullable=False)
    expiration_date = Column(INTEGER(11), nullable=False)

    @hybrid_property
    def effective_dt(self):
        """Hybrid property returning Python datetime object of the season start"""
        return datetime.datetime.fromtimestamp(self.effective_date)

    @hybrid_property
    def effective_delta(self):
        """Hybrid property returning Python time delta since season started"""
        return datetime.datetime.now() - self.effective_dt

    @hybrid_property
    def effective(self):
        """Hybrid property returning stringified approximate Python timedelta since season started"""
        return delta.stringify(self.effective_delta)

    @hybrid_property
    def expiration_dt(self):
        """Hybrid property returning Python datetime object of the season end"""
        return datetime.datetime.fromtimestamp(self.expiration_date)

    @hybrid_property
    def expiration_delta(self):
        """Hybrid property returning time delta until season ends"""
        return self.expiration_dt - datetime.datetime.now()

    @hybrid_property
    def expires(self):
        """Hybrid property returning stringified approximate Python timedelta until season ends"""
        return delta.stringify(self.expiration_delta)

    def __repr__(self):
        return f'<Season> ID {self.season_id} / Active: {self.is_active} / ' \
            f'Effective: "{self.effective}" ("{self.effective_dt}") - ' \
            f'Delta: "{self.effective_delta}") / Expire: "{self.expires}" ' \
            f'("{self.expiration_dt}") - Delta: "{self.expiration_delta}"'


class Player(Base):
    """
    Player database class
    An in-game player, which belongs to an account
    """
    __tablename__           = 'players'

    id                      = Column(INTEGER(11), primary_key=True)
    account_id              = Column(
                                ForeignKey('accounts.account_id',
                                    ondelete='CASCADE', onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    name                    = Column(String(15),
                                nullable=False, unique=True, server_default=FetchedValue())
    create_ident            = Column(String(10), nullable=False, server_default=FetchedValue())
    last_isp                = Column(String(30), nullable=False, server_default=FetchedValue())
    description             = Column(String(240))
    title                   = Column(String(45), nullable=False, server_default=FetchedValue())
    poofin                  = Column(String(80), nullable=False, server_default=FetchedValue())
    poofout                 = Column(String(80), nullable=False, server_default=FetchedValue())
    bankacc                 = Column(INTEGER(11), nullable=False)
    logon_delay             = Column(SMALLINT(6), nullable=False)
    true_level              = Column(INTEGER(11), nullable=False)
    renown                  = Column(INTEGER(11), nullable=False)
    prompt                  = Column(String(42), nullable=False, server_default=FetchedValue())
    remorts                 = Column(INTEGER(11), nullable=False)
    favors                  = Column(INTEGER(11), nullable=False)
    birth                   = Column(INTEGER(11), nullable=False)
    logon                   = Column(INTEGER(11), nullable=False)
    online                  = Column(INTEGER(11))
    logout                  = Column(INTEGER(11), nullable=False)
    bound_room              = Column(INTEGER(11), nullable=False)
    load_room               = Column(INTEGER(11), nullable=False)
    wimpy                   = Column(SMALLINT(6))
    invstart_level          = Column(INTEGER(11))
    color_scheme            = Column(SMALLINT(6))
    sex                     = Column(TINYINT(3), nullable=False)
    race_id                 = Column(
                                ForeignKey('races.race_id',
                                    ondelete='CASCADE', onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    class_id                = Column(
                                ForeignKey('classes.class_id',
                                    ondelete='CASCADE', onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    level                   = Column(INTEGER(11), nullable=False)
    weight                  = Column(SMALLINT(6), nullable=False)
    height                  = Column(SMALLINT(6), nullable=False)
    align                   = Column(SMALLINT(6), nullable=False)
    comm                    = Column(SMALLINT(6), nullable=False)
    karma                   = Column(SMALLINT(6), nullable=False)
    experience_points       = Column(INTEGER(11), nullable=False)
    money                   = Column(INTEGER(11), nullable=False)
    fg_color                = Column(SMALLINT(6), nullable=False)
    bg_color                = Column(SMALLINT(6), nullable=False)
    login_failures          = Column(SMALLINT(6), nullable=False)
    create_haddr            = Column(INTEGER(11), nullable=False)
    auto_level              = Column(INTEGER(11), nullable=False)
    login_fail_haddr        = Column(INTEGER(11))
    last_haddr              = Column(INTEGER(11))
    last_ident              = Column(String(10), server_default=FetchedValue())
    load_room_next          = Column(INTEGER(11))
    load_room_next_expires  = Column(INTEGER(11))
    aggro_until             = Column(INTEGER(11))
    inn_limit               = Column(SMALLINT(6), nullable=False)
    held_xp                 = Column(INTEGER(11))
    last_isp_change         = Column(INTEGER(11))
    perm_hit_pts            = Column(INTEGER(11), nullable=False)
    perm_move_pts           = Column(INTEGER(11), nullable=False)
    perm_spell_pts          = Column(INTEGER(11), nullable=False)
    perm_favor_pts          = Column(INTEGER(11), nullable=False)
    curr_hit_pts            = Column(INTEGER(11), nullable=False)
    curr_move_pts           = Column(INTEGER(11), nullable=False)
    curr_spell_pts          = Column(INTEGER(11), nullable=False)
    curr_favor_pts          = Column(INTEGER(11), nullable=False)
    init_strength           = Column(TINYINT(4), nullable=False)
    init_agility            = Column(TINYINT(4), nullable=False)
    init_endurance          = Column(TINYINT(4), nullable=False)
    init_perception         = Column(TINYINT(4), nullable=False)
    init_focus              = Column(TINYINT(4), nullable=False)
    init_willpower          = Column(TINYINT(4), nullable=False)
    curr_strength           = Column(TINYINT(4), nullable=False)
    curr_agility            = Column(TINYINT(4), nullable=False)
    curr_endurance          = Column(TINYINT(4), nullable=False)
    curr_perception         = Column(TINYINT(4), nullable=False)
    curr_focus              = Column(TINYINT(4), nullable=False)
    curr_willpower          = Column(TINYINT(4), nullable=False)
    is_deleted              = Column(TINYINT(4), nullable=False, server_default=FetchedValue())
    deaths                  = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    total_renown            = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    quests_completed        = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    challenges_completed    = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    def get_flag(self, flag_name=None):
        """Method to return boolean for a specific player flag, by its flag name"""

        # Ensure a flag name string was passed, and find its ID
        if flag_name and isinstance(flag_name, str):
            player_flag     = PlayerFlag.query.filter_by(
                                name    = flag_name
                            ).first()

            # Find the flag value for the player, and return True if the flag value is 1
            if player_flag.flag_id and isinstance(player_flag.flag_id, int):
                players_flag    = PlayersFlag.query.filter_by(
                                    flag_id     = player_flag.flag_id,
                                    player_id   = self.id
                                ).first()
                if players_flag.value == 1:
                    return True
        return False

    @hybrid_property
    def birth_dt(self):
        """Hybrid property returning Python datetime of player birth"""
        return datetime.datetime.fromtimestamp(self.birth)

    @hybrid_property
    def birth_delta(self):
        """Hybrid property returning Python timedelta since player birth"""
        return datetime.datetime.now() - self.birth_dt


    @hybrid_property
    def birth_ago(self):
        """Hybrid property returning stringified approximate Python timedelta since player birth"""
        return delta.stringify(self.birth_delta)

    @hybrid_property
    def logon_dt(self):
        """Hybrid property returning Python datetime of last player log on"""
        return datetime.datetime.fromtimestamp(self.logon)

    hybrid_property
    def logon_delta(self):
        """Hybrid property returning Python timedelta since player log on"""
        return datetime.datetime.now() - self.logon_dt

    @hybrid_property
    def logon_ago(self):
        """Hybrid property returning stringified approximate Python timedelta since player log on"""
        return delta.stringify(self.logon_delta)

    @hybrid_property
    def logout_dt(self):
        """Hybrid property returning Python datetime of last player log out"""
        return datetime.datetime.fromtimestamp(self.logout)

    @hybrid_property
    def logout_delta(self):
        """Hybrid property returning Python timedelta since player log out"""
        return datetime.datetime.now() - self.logout_dt

    @hybrid_property
    def logout_ago(self):
        """Hybrid property returning stringified approximate Python timedelta since player log out"""
        return delta.stringify(self.logout_delta)

    @hybrid_property
    def online_delta(self):
        """Hybrid property returning Python timedelta of player total online time"""
        try:
            return datetime.timedelta(seconds=self.online)
        except:
            return datetime.timedelta(seconds=0)

    @hybrid_property
    def online_time(self):
        """
        Hybrid property returning stringified approximate
            Python timedelta of player total online time
        """
        return delta.stringify(self.online_delta)

    @hybrid_property
    def is_god(self):
        """Hybrid property returning boolean whether player is a "God" """
        if self.true_level >= levels.god_level:
            return True
        return False

    @hybrid_property
    def is_immortal(self):
        """Hybrid property returning boolean whether player is an immortal"""
        if self.true_level in levels.types.keys():
            return True
        return False

    @hybrid_property
    def is_survival(self):
        """
        Hybrid property returning boolean whether
            player is a survival ("PERM_DEATH") character
        """
        return self.get_flag('PERM_DEATH')

    @hybrid_property
    def player_alignment(self):
        """Hybrid property to return player alignment"""
        if self.align <= -1000:
            return 'Very Evil'
        elif self.align > -1000 and self.align <= -500:
            return 'Evil'
        elif self.align > -500 and self.align <= -250:
            return 'Slightly Evil'
        elif self.align > -250 and self.align < 250:
            return 'Neutral'
        elif self.align >= 250 and self.align < 500:
            return 'Slightly Good'
        elif self.align >= 500 and self.align < 1000:
            return 'Good'
        elif self.align >= 1000:
            return 'Very Good'
        else:
            return 'Unknown'

    @hybrid_property
    def player_css(self):
        """Hybrid property to return player CSS class"""
        return self.player_type.lower() + '-player'

    @hybrid_property
    def player_link(self):
        """Hybrid property to return player link"""
        url     = url_for('show_player', player_name=self.name)
        return f'<a href="{url}">{self.name}</a>'

    @hybrid_property
    def player_title(self):
        """Hybrid property to return player title"""
        title   = self.title
        return title.replace('%s', self.player_link)

    @hybrid_property
    def player_type(self):
        """Hybrid property to return player "type" """
        if self.true_level in levels.types.keys():
            return levels.types[self.true_level]
        elif self.is_deleted:
            return 'Dead'
        elif self.is_survival:
            return 'Survival'
        else:
            return 'Classic'

    @hybrid_property
    def seasonal_earned(self):
        """Hybrid property returning the amount of essence earned for the player"""
        # Start with two (2) points for existing, with renown/remort equation
        earned  = int(self.total_renown / 10) + 2
        if self.remorts > 0:
            earned  += int(self.remorts / 5) * 3 + 1
        return earned
