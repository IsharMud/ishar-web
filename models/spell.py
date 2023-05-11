"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, Index, String, Table, Text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from database import Base, metadata


class Force(Base):
    """Force"""
    __tablename__ = 'forces'

    id = Column(INTEGER(11), primary_key=True)
    force_name = Column(String(255), unique=True)

    spells = relationship(
        'SpellInfo',
        secondary='spell_forces'
    )


class SpellFlag(Base):
    """Spell Flag"""
    __tablename__ = 'spell_flags'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))

    spells = relationship(
        'SpellInfo',
        secondary='spells_spell_flags'
    )

    def __repr__(self):
        return f'<SpellFlag> "{self.name}" ({self.id}) : {self.spells}'


class SpellInfo(Base):
    """Spell Info"""
    __tablename__ = 'spell_info'

    id = Column(INTEGER(11), primary_key=True)
    enum_symbol = Column(String(255), nullable=False)
    func_name = Column(String(255))
    skill_name = Column(Text)
    min_posn = Column(INTEGER(11))
    min_use = Column(INTEGER(11))
    spell_breakpoint = Column(INTEGER(11))
    held_cost = Column(INTEGER(11))
    wearoff_msg = Column(Text)
    chant_text = Column(Text)
    difficulty = Column(INTEGER(11))
    rate = Column(INTEGER(11))
    notice_chance = Column(INTEGER(11))
    appearance = Column(Text)
    component_type = Column(INTEGER(11))
    component_value = Column(INTEGER(11))
    scale = Column(INTEGER(11))
    mod_stat_1 = Column(INTEGER(11))
    mod_stat_2 = Column(INTEGER(11))
    is_spell = Column(TINYINT(1))
    is_skill = Column(TINYINT(1))
    is_type = Column(TINYINT(1))
    decide_func = Column(Text, nullable=False)

    def __repr__(self):
        return (f'<SpellInfo> "{self.skill_name}" ({self.id}) '
                f': {self.spells}')


t_spell_forces = Table(
    'spell_forces', metadata,
    Column('spell_id', ForeignKey('spell_info.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('force_id', ForeignKey('forces.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Index('spell_id_2', 'spell_id', 'force_id', unique=True)
)


t_spells_spell_flags = Table(
    'spells_spell_flags', metadata,
    Column('spell_id', ForeignKey('spell_info.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('flag_id', ForeignKey('spell_flags.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_spell_info_bck = Table(
    'spell_info_bck', metadata,
    Column('id', INTEGER(11), nullable=False),
    Column('enum_symbol', String(255), nullable=False),
    Column('func_name', String(255)),
    Column('skill_name', Text),
    Column('min_posn', INTEGER(11)),
    Column('min_use', INTEGER(11)),
    Column('spell_breakpoint', INTEGER(11)),
    Column('held_cost', INTEGER(11)),
    Column('wearoff_msg', Text),
    Column('chant_text', Text),
    Column('difficulty', INTEGER(11)),
    Column('rate', INTEGER(11)),
    Column('notice_chance', INTEGER(11)),
    Column('appearance', Text),
    Column('component_type', INTEGER(11)),
    Column('component_value', INTEGER(11)),
    Column('scale', INTEGER(11)),
    Column('mod_stat_1', INTEGER(11)),
    Column('mod_stat_2', INTEGER(11)),
    Column('is_spell', TINYINT(1)),
    Column('is_skill', TINYINT(1)),
    Column('is_type', TINYINT(1)),
    Column('decide_func', Text, nullable=False)
)
