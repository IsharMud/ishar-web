"""Database classes/models"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from database import Base, metadata


class PlayerSkill(Base):
    __tablename__ = 'player_skills'

    skill_id = Column(ForeignKey('spell_info.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    skill_level = Column(TINYINT(11), nullable=False)

    player = relationship(
        'Player'
    )
    skill = relationship(
        'SpellInfo'
    )
