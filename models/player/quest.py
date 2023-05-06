"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, Table, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from database import Base, metadata
from . import Player


class PlayerQuest(Base):
    __tablename__ = 'player_quests'

    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    status = Column(TINYINT(11), nullable=False)
    last_completed_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    num_completed = Column(TINYINT(4), nullable=False, server_default=text("0"))

    player = relationship(
        'Player',
        back_populates='quests',
        single_parent=True,
        uselist=False
    )

    quest = relationship(
        'Quest',
        single_parent=True,
        uselist=False
    )

    def __repr__(self):
        return (f'<PlayerQuest> {self.quest} / '
                f'Status: {self.status} / '
                f'Last Completed: {self.last_completed_at} / '
                f'Num Completed: {self.num_completed} @ {self.player}')


class PlayerQuestStep(Base):
    __tablename__ = 'player_quest_steps'

    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    step_id = Column(ForeignKey('quest_steps.step_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    num_collected = Column(TINYINT(1), nullable=False)

    player = relationship(
        'Player',
        single_parent=True,
        uselist=False
    )

    step = relationship(
        'QuestStep',
        single_parent=True,
        uselist=False,
    )

    def __repr__(self):
        return (f'<PlayerQuestStep> {self.step} / '
                f'Num Completed: {self.num_collected} @ '
                f'{self.player}')
