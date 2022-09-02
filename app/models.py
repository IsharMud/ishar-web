from app import app
import crypt
import hmac
import levels
from flask import url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, ForeignKey, String, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

# Connect to the database
db = SQLAlchemy(app)


# Account database class
class Account(db.Model, UserMixin):
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

    # flask-login method to return account ID
    def get_id(self):
        return str(self.account_id)

    # flask-login method to return boolean whether user is authenticated
    def is_authenticated(self):
        return isinstance(self.account_id, int)

    # flask-login method to return boolean whether user is active
    def is_active(self):
        return isinstance(self.account_id, int)

    # Hybrid property returning boolean whether user is an admin
    @hybrid_property
    def is_admin(self):
        for player in self.players:
            if player.is_god:
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
        return False

    # Method to check an account password
    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)

    # Method to create new account
    def create_account(self):
        try:

            # Hash the password and add the account to the database
            self.password = crypt.crypt(self.password, crypt.mksalt(method=crypt.METHOD_MD5))
            db.session.add(self)
            db.session.commit()

            # Start each available account upgrade at zero (0)
            for init_ugrade in AccountUpgrade.query.all():
                create_upgrade  = AccountsUpgrade(
                    account_upgrades_id     = init_ugrade.id,
                    account_id              = self.account_id,
                    amount                  = 0
                )
                db.session.add(create_upgrade)
            db.session.commit()

            # Return the new account ID
            return self.account_id

        except Exception as e:
            print(e)
        return False

    # Hybrid property containing the amount of essence earned for the account
    @hybrid_property
    def seasonal_earned(self):

        # Start at zero (0), and return the points from the player within the account whom has earned the highest amount
        s = 0
        for player in self.players:
            if player.seasonal_earned > s:
                s = player.seasonal_earned
        return s

    def __repr__(self):
        return f'<Account> "{self.account_name}" ({self.account_id})'


# Account Upgrade database class
class AccountUpgrade(db.Model):
    __tablename__   = 'account_upgrades'
    id                  = Column(TINYINT(4), primary_key=True)
    cost                = Column(MEDIUMINT(4), nullable=False)
    description         = Column(String(200), nullable=False)
    name                = Column(String(30), nullable=False, unique=True)
    max_value           = Column(MEDIUMINT(4), nullable=False, server_default=FetchedValue())

    accounts_upgrade    = relationship('AccountsUpgrade', backref='upgrade')

    def __repr__(self):
        return f'<AccountUpgrade> "{self.name}" ({self.id}) / Cost: {self.cost} / Max Value: {self.max_value}'


# Accounts Upgrade database class
class AccountsUpgrade(db.Model):
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

    # Method to increment an account upgrade and reduce account seasonal points (essence)
    def do_upgrade(self, increment=1):
        try:
            self.amount = self.amount + increment
            self.account.seasonal_points = self.account.seasonal_points - self.upgrade.cost
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def __repr__(self):
        return f'<AccountsUpgrade> "{self.upgrade.name}" ({self.account_upgrades_id}) @ <Account> "{self.account.account_name}" ({self.account_id}) / Amount: {self.amount}'


# Affect Flag database class (unused)
class AffectFlag(db.Model):
    __tablename__   = 'affect_flags'

    flag_id = Column(TINYINT(4), primary_key=True)
    name    = Column(String(30), nullable=False, unique=True)

    def __repr__(self):
        return f'<AffectFlag> "{self.name}" ({self.flag_id})'


# Board database class (unused)
class Board(db.Model):
    __tablename__   = 'boards'

    board_id    = Column(TINYINT(4), primary_key=True)
    board_name  = Column(String(15), nullable=False)

    def __repr__(self):
        return f'<Board> "{self.board_name}" ({self.board_id})'


# Challenge database class
class Challenge(db.Model):
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

    def __repr__(self):
        return f'<Challenge> "{self.mob_name}" ({self.challenge_id}) / Active: {self.is_active} / Winner: "{self.winner_desc}"'


# Condition database class (unused)
class Condition(db.Model):
    __tablename__   = 'conditions'

    condition_id    = Column(TINYINT(4), primary_key=True)
    name            = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<PlayerCondition> "{self.name}" ({self.condition_id})'


# DisplayOption database class (unused)
class DisplayOption(db.Model):
    __tablename__   = 'display_options'

    display_id  = Column(TINYINT(4), primary_key=True)
    name        = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<DisplayOption> "{self.name}" ({self.display_id})'


# News database class
class News(db.Model):
    __tablename__   = 'news'

    news_id     = Column(INTEGER(11), primary_key=True)
    account_id  = Column(
                    ForeignKey('accounts.account_id',
                        ondelete='CASCADE', onupdate='CASCADE'
                    ), nullable=False, index=True
                )
    created_at  = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    subject     = Column(String(64), nullable=False, server_default=FetchedValue())
    body        = Column(Text, nullable=False)

    account     = relationship('Account')

    # Method to add a news post
    def add_news(self, subject=None, body=None):
        try:
            db.session.add(self)
            db.session.commit()
            return self.news_id
        except Exception as e:
            print(e)
        return False

    def __repr__(self):
        return f'<News> "{self.subject}" ({self.news_id}) / by "{self.account.name}" / at "{self.created_at}"'


# Player Class database class
class PlayerClass(db.Model):
    __tablename__   = 'classes'

    class_id            = Column(TINYINT(3), primary_key=True)
    class_name          = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    class_display       = Column(String(32))
    class_description   = Column(String(64))

    player_class        = relationship('Player', backref='class')

    def __repr__(self):
        return f'<PlayerClass> "{self.class_name}" ({self.class_id})'


# Player Flag database class
class PlayerFlag(db.Model):
    __tablename__   = 'player_flags'

    flag_id = Column(INTEGER(11), primary_key=True)
    name    = Column(String(20), nullable=False, unique=True)

    flag    = relationship('PlayersFlag', backref='flag')

    def __repr__(self):
        return f'<PlayerFlag> "{self.name}" ({self.flag_id})'


# Players Flag database class
class PlayersFlag(db.Model):
    __tablename__   = 'player_player_flags'

    flag_id     = Column(
                    ForeignKey('player_flags.flag_id',
                        ondelete='CASCADE', onupdate='CASCADE'
                    ), nullable=False, index=True, primary_key=True
                )
    player_id   = Column(
                    ForeignKey('players.id',
                        ondelete='CASCADE', onupdate='CASCADE'
                    ), nullable=False, index=True, primary_key=True
                )
    value       = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    player      = relationship('Player', backref='flags')

    def __repr__(self):
        return f'<PlayersFlag> "{self.flag.name}" ({self.flag_id}) @ <Player> "{self.player.name}" ({self.player_id}) : {self.value}'


# Player Race database class
class PlayerRace(db.Model):
    __tablename__   = 'races'

    race_id             = Column(TINYINT(3), primary_key=True)
    race_name           = Column(String(15), nullable=False, unique=True)
    race_description    = Column(String(64))

    player_race = relationship('Player', backref='race')

    def __repr__(self):
        return f'<PlayerRace> "{self.race_name}" ({self.race_id})'


# Quest database class
class Quest(db.Model):
    __tablename__   = 'quests'

    quest_id            = Column(INTEGER(11), primary_key=True)
    name                = Column(String(25), nullable=False, unique=True, server_default=FetchedValue())
    display_name        = Column(String(30), nullable=False)
    is_major            = Column(TINYINT(1), nullable=False, server_default=FetchedValue())
    xp_reward           = Column(INTEGER(11), nullable=False, server_default=FetchedValue())
    completion_message  = Column(String(80), nullable=False)

    def __repr__(self):
        return f'<Quest> "{self.name}" ({self.quest_id}) / "{self.display_name}" / XP: {self.xp_reward}'


# Player Quest database class
class PlayerQuest(db.Model):
    __tablename__   = 'player_quests'

    quest_id    = Column(
                    ForeignKey('quests.quest_id',
                        ondelete='CASCADE', onupdate='CASCADE'
                    ), nullable=False, index=True, primary_key=True
                )
    player_id   = Column(
                    ForeignKey('players.id',
                        ondelete='CASCADE', onupdate='CASCADE'
                    ), nullable=False, index=True, primary_key=True
                )
    value       = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    quest       = relationship('Quest')
    player      = relationship('Player', backref='quests')

    def __repr__(self):
        return f'<PlayerQuest> "{self.quest.name}" ({self.quest_id}) @ <Player> "{self.player.name}" ({self.player_id}) / Value: {self.value}'


# Remort Upgrades database class
class RemortUpgrade(db.Model):
    __tablename__   = 'remort_upgrades'

    upgrade_id      = Column(INTEGER(11), primary_key=True)
    name            = Column(String(20), nullable=False, unique=True, server_default=FetchedValue())
    renown_cost     = Column(SMALLINT(6), nullable=False)
    max_value       = Column(SMALLINT(6), nullable=False)

    remort_upgrades = relationship('PlayerRemortUpgrade', backref='remort_upgrade')

    def __repr__(self):
        return f'<RemortUpgrade> "{self.name}" ({self.upgrade_id}) / Cost: {self.renown_cost} / Max: {self.max_value}'


# Player Remort Upgrades database class
class PlayerRemortUpgrade(db.Model):
    __tablename__   = 'player_remort_upgrades'

    upgrade_id  = Column(
                    ForeignKey('remort_upgrades.upgrade_id',
                        ondelete='CASCADE', onupdate='CASCADE'
                    ), nullable=False, index=True, primary_key=True
                )
    player_id   = Column(
                    ForeignKey('players.id',
                        ondelete='CASCADE', onupdate='CASCADE'
                    ), nullable=False, index=True, primary_key=True
                )
    value       = Column(INTEGER(11), nullable=False, server_default=FetchedValue())

    player      = relationship('Player', backref='remort_upgrades')

    def __repr__(self):
        return f'<PlayerRemortUpgrade> "{self.remort_upgrade.name}" ({self.upgrade_id}) @ <Player> "{self.player.name}" ({self.player_id}) / Value: {self.value}'


# Season database class
class Season(db.Model):
    __tablename__   = 'seasons'

    season_id       = Column(INTEGER(11), primary_key=True)
    is_active       = Column(TINYINT(4), nullable=False)
    effective_date  = Column(INTEGER(11), nullable=False)
    expiration_date = Column(INTEGER(11), nullable=False)

    def __repr__(self):
        return f'<Season> ID {self.season_id} / Active: {self.is_active} / Effective: {self.effective_date} / Expiration: {self.expiration_date}'


# Skill database class (unused)
class Skill(db.Model):
    __tablename__   = 'skills'

    skill_id        = Column(INTEGER(11), primary_key=True)
    class_id        = Column(
                        ForeignKey('classes.class_id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True
                    )
    max_value       = Column(INTEGER(11), nullable=False)
    difficulty      = Column(INTEGER(11), nullable=False)

#    player_skills   = relationship('PlayerSkill', backref='skill')


    def __repr__(self):
        return f'<Skill> ID {self.skill_id} / Class ID {self.class_id} / Max: {self.max_value} / Difficulty: {self.difficulty}'

# Player Skill database class (unused)
class PlayerSkill(db.Model):
    __tablename__   = 'player_skills'

    skill_id        = Column(
                        ForeignKey('skills.skill_id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    player_id       = Column(
                        ForeignKey('players.id',
                            ondelete='CASCADE', onupdate='CASCADE'
                        ), nullable=False, index=True, primary_key=True
                    )
    skill_level     = Column(TINYINT(11), nullable=False, server_default=FetchedValue())

#    player         = relationship('Player', backref='skills')

    def __repr__(self):
        return f'<PlayerSkill> {self.skill_id} @ <Player> "{self.player.name}" ({self.player_id}) / Skill Level: {self.skill_level}'


# Player database class
class Player(db.Model):
    __tablename__   = 'players'

    id                      = Column(INTEGER(11), primary_key=True)
    account_id              = Column(
                                ForeignKey('accounts.account_id',
                                    ondelete='CASCADE', onupdate='CASCADE'
                                ), nullable=False, index=True
                            )
    name                    = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
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

    # Hybrid property returning boolean whether player is a God
    @hybrid_property
    def is_god(self):
        if self.true_level >= levels.god_level:
            return True
        return False

    # Hybrid property returning boolean whether player is an immortal
    @hybrid_property
    def is_immortal(self):
        if self.true_level in levels.types.keys():
            return True
        return False

    # Hybrid property returning boolean whether player is a survival ("PERM_DEATH") character
    @hybrid_property
    def is_survival(self):
        if self.flags[45].flag.name == 'PERM_DEATH' and self.flags[45].value == 1:
            return True
        return False

    # Hybrid property to return player alignment
    @hybrid_property
    def player_alignment(self):
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
    
    # Hybrid property to return player CSS class
    @hybrid_property
    def player_css(self):
        return self.player_type.lower() + '-player'

    # Hybrid property to return player link
    @hybrid_property
    def player_link(self):
        url = url_for('show_player', player_name=self.name)
        return f'<a href="{url}">{self.name}</a>'

    # Hybrid property to return player title
    @hybrid_property
    def player_title(self):
        title   = self.title
        return title.replace('%s', self.player_link)

    # Hybrid property to return player "type"
    @hybrid_property
    def player_type(self):
        if self.true_level in levels.types.keys():
            return levels.types[self.true_level]
        elif self.is_deleted:
            return 'Dead'
        elif self.is_survival:
            return 'Survival'
        else:
            return 'Classic'

    # Hybrid property returning the amount of essence earned for the player
    @hybrid_property
    def seasonal_earned(self):

        # Start with two (2) points for existing, with renown/remort equation
        c = int(self.total_renown / 10) + 2
        if self.remorts > 0:
            c += int(self.remorts / 5) * 3 + 1
        return c
