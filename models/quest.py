"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, Table, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from database import Base, metadata


t_quest_prereqs = Table(
    'quest_prereqs', metadata,
    Column('quest_id', ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('required_quest', ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class QuestReward(Base):
    __tablename__ = 'quest_rewards'

    reward_num = Column(INTEGER(11), primary_key=True, nullable=False)
    reward_type = Column(TINYINT(2), nullable=False)
    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)

    quest = relationship(
        'Quest',
        single_parent=True,
        uselist=False,
        back_populates='rewards'
    )

    def __repr__(self):
        return (f'<QuestReward> {self.reward_num} ({self.reward_type}) @ '
                f'{self.quest}')


class QuestStep(Base):
    __tablename__ = 'quest_steps'

    step_id = Column(TINYINT(4), primary_key=True)
    step_type = Column(TINYINT(4), nullable=False)
    target = Column(INTEGER(11), nullable=False)
    num_required = Column(INTEGER(11), nullable=False)
    quest_id = Column(ForeignKey('quests.quest_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    time_limit = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    mystify = Column(TINYINT(1), nullable=False, server_default=text("0"))
    mystify_text = Column(String(80), nullable=False, server_default=text("''"))

    quest = relationship(
        'Quest',
        single_parent=True,
        uselist=False,
        back_populates='steps'
    )

    def __repr__(self):
        return (f'<QuestStep> {self.step_id} ({self.step_type}) / '
                f'Target: {self.target} [{self.num_required}] @ '
                f'{self.quest}')


class Quest(Base):
    __tablename__ = 'quests'

    quest_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False, unique=True, server_default=text("''"))
    display_name = Column(String(30), nullable=False)
    completion_message = Column(String(80), nullable=False)
    min_level = Column(TINYINT(4), nullable=False, server_default=text("1"))
    max_level = Column(TINYINT(4), nullable=False, server_default=text("20"))
    repeatable = Column(TINYINT(1), nullable=False, server_default=text("0"))
    description = Column(String(512), nullable=False, server_default=text("'No description available.'"))
    prerequisite = Column(INTEGER(11), nullable=False, server_default=text("-1"))
    # class_restrict = Column(TINYINT(4), nullable=False, server_default=text("-1"))
    class_restrict = Column(ForeignKey('classes.class_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    quest_intro = Column(String(1600), nullable=False, server_default=text("''"))

    parents = relationship(
        'Quest',
        secondary='quest_prereqs',
        primaryjoin='Quest.quest_id == quest_prereqs.c.quest_id',
        secondaryjoin='Quest.quest_id == quest_prereqs.c.required_quest'
    )

    restricted_class = relationship(
        'Class',
        single_parent=True,
        uselist=False
    )

    rewards = relationship(
        'QuestReward',
        single_parent=True,
        uselist=True,
        back_populates='quest'
    )

    steps = relationship(
        'QuestStep',
        back_populates='quest',
        single_parent=True,
        uselist=True
    )

    def __repr__(self):
        return (f'<Quest> {self.name} ({self.quest_id}) / '
                f'Levels: {self.min_level} - {self.max_level} / '
                f'Parents: {len(self.parents)} / '
                f'Steps: {len(self.steps)} / '
                f'Class: {self.restricted_class}')
