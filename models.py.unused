"""
TODO: Unused models below
There is eventually a place for all of these... somewhere... somehow - plus more!
"""

# Affect Flag database class (unused)
#class AffectFlag(Base):
#    __tablename__   = 'affect_flags'

#    flag_id = Column(TINYINT(4), primary_key=True)
#    name    = Column(String(30), nullable=False, unique=True)

#    def __repr__(self):
#        return f'<AffectFlag> "{self.name}" ({self.flag_id})'


# Board database class (unused)
#class Board(Base):
#    __tablename__  = 'boards'

#    board_id       = Column(TINYINT(4), primary_key=True)
#    board_name     = Column(String(15), nullable=False)

#    def __repr__(self):
#        return f'<Board> "{self.board_name}" ({self.board_id})'


# Condition database class (unused)
#class Condition(Base):
#    __tablename__   = 'conditions'

#    condition_id    = Column(TINYINT(4), primary_key=True)
#    name            = Column(String(20), nullable=False, unique=True)

#    def __repr__(self):
#        return f'<PlayerCondition> "{self.name}" ({self.condition_id})'


# DisplayOption database class (unused)
#class DisplayOption(Base):
#    __tablename__  = 'display_options'

#    display_id     = Column(TINYINT(4), primary_key=True)
#    name           = Column(String(20), nullable=False, unique=True)

#    def __repr__(self):
#        return f'<DisplayOption> "{self.name}" ({self.display_id})'


# Skill database class (unused)
#class Skill(Base):
#    __tablename__   = 'skills'

#    skill_id        = Column(INTEGER(11), primary_key=True)
#    class_id        = Column(
#                        ForeignKey('classes.class_id',
#                            ondelete='CASCADE', onupdate='CASCADE'
#                        ), nullable=False, index=True
#                    )
#    max_value       = Column(INTEGER(11), nullable=False)
#    difficulty      = Column(INTEGER(11), nullable=False)

#    player_skills   = relationship('PlayerSkill', backref='skill')


#    def __repr__(self):
#        return f'<Skill> ID {self.skill_id} / Class ID {self.class_id} / Max: {self.max_value} / Difficulty: {self.difficulty}'

# Player Skill database class (unused)
#class PlayerSkill(Base):
#    __tablename__  = 'player_skills'

#    skill_id       = Column(
#                        ForeignKey('skills.skill_id',
#                            ondelete='CASCADE', onupdate='CASCADE'
#                        ), nullable=False, index=True, primary_key=True
#                    )
#    player_id      = Column(
#                        ForeignKey('players.id',
#                            ondelete='CASCADE', onupdate='CASCADE'
#                        ), nullable=False, index=True, primary_key=True
#                    )
#    skill_level    = Column(TINYINT(11), nullable=False, server_default=FetchedValue())

#    player         = relationship('Player', backref='skills')

#    def __repr__(self):
#        return f'<PlayerSkill> {self.skill_id} @ <Player> "{self.player.name}" ({self.player_id}) / Skill Level: {self.skill_level}'
