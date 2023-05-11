"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT

from database import Base, metadata


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
