"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, Text, text  # , Table
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship

from database import Base, metadata
from models.race import Race


class Class(Base):
    """Classes available when creating a player character:
        such as Cleric, Magician, Warrior, etc."""
    __tablename__ = 'classes'

    class_id = Column(TINYINT(3), primary_key=True)
    class_name = Column(String(15), nullable=False, unique=True,
                        server_default=text("'NO_CLASS'"))
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
        'Player',
        back_populates='common',
        single_parent=True,
        uselist=False
    )

    player_class = relationship(
        'Class',
        single_parent=True,
        uselist=False
    )

    player_race = relationship(
        'Race',
        single_parent=True,
        uselist=False
    )

    def __repr__(self):
        return (f'<PlayerCommon> {self.player} / {self.player_class} / '
                f'{self.player_race}')
