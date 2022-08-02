from app import app
import crypt
import hmac
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, Column, DateTime, ForeignKey, Integer, MetaData, SmallInteger, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

# Connect to the database
db = SQLAlchemy(app)

# Account database class
class Account(db.Model, UserMixin):
    __tablename__   = 'accounts'
    account_id      = Column(Integer, primary_key=True)
    created_at      = Column(DateTime, nullable=False, server_default=FetchedValue())
    seasonal_points = Column(Integer, nullable=False, server_default=FetchedValue())
    email           = Column(String(30), nullable=False, unique=True)
    password        = Column(String(36), nullable=False)
    create_isp      = Column(String(25), nullable=False)
    last_isp        = Column(String(25), nullable=False)
    create_ident    = Column(String(25), nullable=False)
    last_ident      = Column(String(25), nullable=False)
    create_haddr    = Column(Integer, nullable=False)
    last_haddr      = Column(Integer, nullable=False)
    account_name    = Column(String(25), nullable=False, unique=True)
    players         = relationship('Player', backref='account')

    def get_id(self):
        return str(self.account_id)

    def is_authenticated(self):
        return isinstance(self.account_id, int)

    def is_active(self):
        return isinstance(self.account_id, int)

    # Accounts with a player above a certain level are administrators
    def is_admin(self, admin_level):
        for player in self.players:
            if player.true_level > admin_level:
                return True

        return False

    # Method to allow users to change their account password
    def change_password(self, new_password):
        try:
            self.password = crypt.crypt(new_password, crypt.mksalt(method=crypt.METHOD_MD5))
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return e

    # Method to check an account password
    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)

    # Method to create new account
    def create_account(self):
        try:
            self.password = crypt.crypt(self.password, crypt.mksalt(method=crypt.METHOD_MD5))
            db.session.add(self)
            db.session.commit()
            return self.account_id
        except Exception as e:
            print(e)
            return e

    def __repr__(self):
        return f'<Account> "{self.account_name}" ("{self.account_id}")'


# Player Flag database class
class PlayerFlag(db.Model):
    __tablename__   = 'player_flags'
    flag_id         = Column(Integer, primary_key=True)
    name            = Column(String(20), nullable=False, unique=True)
    flag            = relationship('PlayersFlags', backref='flag')

    def __repr__(self):
        return f'<PlayerFlag> "{self.name}" ("{self.flag_id}")'

# Players Flags database class
class PlayersFlags(db.Model):
    __tablename__   = 'player_player_flags'
    flag_id         = Column(
                        ForeignKey('player_flags.flag_id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    value           = Column(Integer)
    player          = relationship('Player', backref='flags')

    def __repr__(self):
        return f'<PlayersFlags> "{self.flag_id}" @ <Player> "{self.player_id}" : "{self.value}"'

# Player Class database class
class PlayerClass(db.Model):
    __tablename__   = 'classes'
    class_id        = Column(Integer, primary_key=True)
    class_name      = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    player_class    = relationship('Player', backref='class')

    def __repr__(self):
        return f'<PlayerClass "{self.class_name}" @ "{self.class_id}"'

# Player Race database class
class PlayerRace(db.Model):
    __tablename__   = 'races'
    race_id         = Column(Integer, primary_key=True)
    race_name       = Column(String(15), nullable=False, unique=True)
    player_race     = relationship('Player', backref='race')

    def __repr__(self):
        return f'<PlayerRace "{self.race_name}" @ "{self.race_id}"'

# Player database class
class Player(db.Model):
    __tablename__           = 'players'
    id                      = Column(Integer, primary_key=True)
    account_id              = Column(
                                ForeignKey('accounts.account_id',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    name                    = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    create_ident            = Column(String(10), nullable=False, server_default=FetchedValue())
    last_isp                = Column(String(30), nullable=False, server_default=FetchedValue())
    description             = Column(String(240))
    title                   = Column(String(45), nullable=False, server_default=FetchedValue())
    poofin                  = Column(String(80), nullable=False, server_default=FetchedValue())
    poofout                 = Column(String(80), nullable=False, server_default=FetchedValue())
    bankacc                 = Column(Integer, nullable=False)
    logon_delay             = Column(SmallInteger, nullable=False)
    true_level              = Column(Integer, nullable=False)
    renown                  = Column(Integer, nullable=False)
    prompt                  = Column(String(42), nullable=False, server_default=FetchedValue())
    remorts                 = Column(Integer, nullable=False)
    favors                  = Column(Integer, nullable=False)
    birth                   = Column(Integer, nullable=False)
    logon                   = Column(Integer, nullable=False)
    online                  = Column(Integer)
    logout                  = Column(Integer, nullable=False)
    bound_room              = Column(Integer, nullable=False)
    load_room               = Column(Integer, nullable=False)
    wimpy                   = Column(SmallInteger)
    invstart_level          = Column(Integer)
    color_scheme            = Column(SmallInteger)
    sex                     = Column(Integer, nullable=False)
    race_id                 = Column(
                                ForeignKey('races.race_id',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    class_id                = Column(
                                ForeignKey('classes.class_id',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    level                   = Column(Integer, nullable=False)
    weight                  = Column(SmallInteger, nullable=False)
    height                  = Column(SmallInteger, nullable=False)
    align                   = Column(SmallInteger, nullable=False)
    comm                    = Column(SmallInteger, nullable=False)
    karma                   = Column(SmallInteger, nullable=False)
    experience_points       = Column(Integer, nullable=False)
    money                   = Column(Integer, nullable=False)
    fg_color                = Column(SmallInteger, nullable=False)
    bg_color                = Column(SmallInteger, nullable=False)
    login_failures          = Column(SmallInteger, nullable=False)
    create_haddr            = Column(Integer, nullable=False)
    auto_level              = Column(Integer, nullable=False)
    login_fail_haddr        = Column(Integer)
    last_haddr              = Column(Integer)
    last_ident              = Column(String(10), server_default=FetchedValue())
    load_room_next          = Column(Integer)
    load_room_next_expires  = Column(Integer)
    aggro_until             = Column(Integer)
    inn_limit               = Column(SmallInteger, nullable=False)
    held_xp                 = Column(Integer)
    last_isp_change         = Column(Integer)
    perm_hit_pts            = Column(Integer, nullable=False)
    perm_move_pts           = Column(Integer, nullable=False)
    perm_spell_pts          = Column(Integer, nullable=False)
    perm_favor_pts          = Column(Integer, nullable=False)
    curr_hit_pts            = Column(Integer, nullable=False)
    curr_move_pts           = Column(Integer, nullable=False)
    curr_spell_pts          = Column(Integer, nullable=False)
    curr_favor_pts          = Column(Integer, nullable=False)
    init_strength           = Column(Integer, nullable=False)
    init_agility            = Column(Integer, nullable=False)
    init_endurance          = Column(Integer, nullable=False)
    init_perception         = Column(Integer, nullable=False)
    init_focus              = Column(Integer, nullable=False)
    init_willpower          = Column(Integer, nullable=False)
    curr_strength           = Column(Integer, nullable=False)
    curr_agility            = Column(Integer, nullable=False)
    curr_endurance          = Column(Integer, nullable=False)
    curr_perception         = Column(Integer, nullable=False)
    curr_focus              = Column(Integer, nullable=False)
    curr_willpower          = Column(Integer, nullable=False)
    is_deleted              = Column(Integer, nullable=False, server_default=FetchedValue())
    deaths                  = Column(Integer, nullable=False, server_default=FetchedValue())
    total_renown            = Column(Integer, nullable=False, server_default=FetchedValue())
    quests_completed        = Column(Integer, nullable=False, server_default=FetchedValue())
    challenges_completed    = Column(Integer, nullable=False, server_default=FetchedValue())

    # Players above a certain level are administrators
    def is_admin(self, admin_level):
        if self.true_level > admin_level:
                return True

        return False

    def __repr__(self):
        return f'<Player> "{self.name}" ("{self.id}")'


# News database class
class News(db.Model):
    __tablename__   = 'news'
    news_id         = Column(Integer, primary_key=True)
    account_id      = Column(
                        ForeignKey('accounts.account_id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True
                    )
    created_at      = Column(DateTime, nullable=False, server_default=FetchedValue())
    subject         = Column(String(64), nullable=False, server_default=FetchedValue())
    body            = Column(Text, nullable=False)
    account         = relationship('Account')

    # Method to post news
    def add_news(self, subject=None, body=None):
        try:
            db.session.add(self)
            db.session.commit()
            return self.news_id
        except Exception as e:
            print(e)

    def __repr__(self):
        return f'<News> "{self.subject}" ("{self.news_id}")'


# Season database class
class Season(db.Model):
    __tablename__   = 'seasons'
    season_id       = Column(Integer, primary_key=True)
    is_active       = Column(Integer, nullable=False)
    effective_date  = Column(Integer, nullable=False)
    expiration_date = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Season> "{self.season_id}" (until "{self.expiration_date}")'


# Challenge database class
class Challenge(db.Model):
    __tablename__   = 'challenges'
    challenge_id    = Column(SmallInteger, primary_key=True)
    mob_vnum        = Column(Integer, nullable=False)
    orig_level      = Column(Integer, nullable=False)
    orig_people     = Column(Integer, nullable=False)
    orig_tier       = Column(Integer, nullable=False)
    adj_level       = Column(Integer, nullable=False)
    adj_people      = Column(Integer, nullable=False)
    adj_tier        = Column(Integer, nullable=False)
    challenge_desc  = Column(String(80), nullable=False)
    winner_desc     = Column(String(80), nullable=False, server_default=FetchedValue())
    mob_name        = Column(String(30), nullable=False)
    is_active       = Column(Integer, nullable=False, server_default=FetchedValue())

    def __repr__(self):
        return f'<Challenge> "{self.mob_name}" ("{self.challenge_id}")'


# Players Remort Upgrades database class
class PlayersRemortUpgrades(db.Model):
    __tablename__   = 'player_remort_upgrades'
    upgrade_id      = Column(
                        ForeignKey('remort_upgrades.upgrade_id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    value           = Column('value', Integer, nullable=False)
    remort_upgrade  = relationship('RemortUpgrade')
    player          = relationship('Player', backref='remort_upgrades')

    def __repr__(self):
        return f'<PlayersRemortUpgrades> Upgrade ID "{self.upgrade_id}" @ Player "{self.player.name}" (ID: "{self.player_id}") / Value: "{self.value}"'

# Remort Upgrade database class
class RemortUpgrade(db.Model):
    __tablename__   = 'remort_upgrades'
    upgrade_id      = Column(Integer, primary_key=True)
    name            = Column(String(20), nullable=False, unique=True, server_default=FetchedValue())
    renown_cost     = Column(SmallInteger, nullable=False)
    max_value       = Column(SmallInteger, nullable=False)

    def __repr__(self):
        return f'<RemortUpgrade> "{self.name}" (ID: "{self.upgrade_id}") / Cost: "{self.renown_cost}" /  Max Value: "{self.max_value}"'


# Players Quests database class
class PlayersQuests(db.Model):
    __tablename__   = 'player_quests'
    quest_id        = Column(
                        ForeignKey('quests.quest_id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE',
                            onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    value           = Column('value', Integer, nullable=False)
    quest           = relationship('Quest')
    player          = relationship('Player', backref='quests')

    def __repr__(self):
        return f'<PlayersQuests> "{self.quest_id}" @ "{self.player_id}" / "{self.value}"'

# Quest database class
class Quest(db.Model):
    __tablename__       = 'quests'
    quest_id            = Column(Integer, primary_key=True)
    name                = Column(String(25), nullable=False, unique=True, server_default=FetchedValue())
    display_name        = Column(String(30), nullable=False)
    is_major            = Column(Integer, nullable=False, server_default=FetchedValue())
    xp_reward           = Column(Integer, nullable=False, server_default=FetchedValue())
    completion_message  = Column(String(80), nullable=False)

    def __repr__(self):
        return f'<Quest> "{self.name}" ("{self.quest_id}")'
