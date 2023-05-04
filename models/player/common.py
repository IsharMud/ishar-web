"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, Text, text  # , Table
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import backref, relationship

from database import Base, metadata


class PlayerClass(Base):
    """Classes available when creating a player character:
        such as Cleric, Magician, Warrior, etc."""
    __tablename__ = 'classes'

    class_id = Column(TINYINT(3), primary_key=True)
    class_name = Column(String(15), nullable=False, unique=True, server_default=text("'NO_CLASS'"))
    class_display = Column(String(32))
    class_description = Column(String(64))

    @property
    def class_display_name(self):
        """Human-readable display name for a player class"""
        return self.class_name.replace('_', '-').title()

    @property
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

        # Alphabetic as last resort
        return ['Agility', 'Endurance', 'Focus', 'Perception', 'Strength', 'Willpower']

    def __repr__(self):
        return (f'<Class> "{self.class_name}" ({self.class_id})')


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
    is_invertebrae = Column(TINYINT(1), nullable=False, server_default=text("0"))
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


class PlayerCommon(Base):
    """Common data of players that is shared with in-game 'mobiles'"""
    __tablename__ = 'player_common'

    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    class_id = Column(ForeignKey('classes.class_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    race_id = Column(ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
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
        'Player', backref=backref('common', uselist=False)
    )
    player_class = relationship('PlayerClass')
    player_race = relationship('Race')

    def __repr__(self):
        return (f'<PlayerCommon> {self.player} / {self.player_class} / '
                f'{self.player_race}')


# t_player_common = Table(
#     'player_common', metadata,
#     Column('player_id', ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True),
#     Column('class_id', TINYINT(4), nullable=False),
#     Column('race_id', ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
#     Column('sex', TINYINT(4), nullable=False, server_default=text("0")),
#     Column('level', TINYINT(3), nullable=False),
#     Column('weight', SMALLINT(5), nullable=False),
#     Column('height', SMALLINT(5), nullable=False),
#     Column('comm_points', SMALLINT(6), nullable=False),
#     Column('alignment', SMALLINT(6), nullable=False),
#     Column('strength', TINYINT(3), nullable=False),
#     Column('agility', TINYINT(3), nullable=False),
#     Column('endurance', TINYINT(3), nullable=False),
#     Column('perception', TINYINT(3), nullable=False),
#     Column('focus', TINYINT(3), nullable=False),
#     Column('willpower', TINYINT(3), nullable=False),
#     Column('init_strength', TINYINT(3), nullable=False),
#     Column('init_agility', TINYINT(3), nullable=False),
#     Column('init_endurance', TINYINT(3), nullable=False),
#     Column('init_perception', TINYINT(3), nullable=False),
#     Column('init_focus', TINYINT(3), nullable=False),
#     Column('init_willpower', TINYINT(3), nullable=False),
#     Column('perm_hit_pts', SMALLINT(6), nullable=False),
#     Column('perm_move_pts', SMALLINT(6), nullable=False),
#     Column('perm_spell_pts', SMALLINT(6), nullable=False),
#     Column('perm_favor_pts', SMALLINT(6), nullable=False),
#     Column('curr_hit_pts', SMALLINT(6), nullable=False),
#     Column('curr_move_pts', SMALLINT(6), nullable=False),
#     Column('curr_spell_pts', SMALLINT(6), nullable=False),
#     Column('curr_favor_pts', SMALLINT(6), nullable=False),
#     Column('experience', INTEGER(11), nullable=False),
#     Column('gold', MEDIUMINT(9), nullable=False),
#     Column('karma', MEDIUMINT(9), nullable=False)
# )
