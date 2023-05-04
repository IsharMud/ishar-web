"""Database classes/models"""
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT

from database import Base, metadata


class Challenge(Base):
    """Challenge mobiles available for players to kill in-game for rewards"""
    __tablename__ = 'challenges'

    challenge_id = Column(SMALLINT(4), primary_key=True)
    mob_vnum = Column(INTEGER(11), nullable=False)
    orig_level = Column(TINYINT(4), nullable=False)
    orig_people = Column(TINYINT(4), nullable=False)
    orig_tier = Column(TINYINT(4), nullable=False)
    adj_level = Column(TINYINT(4), nullable=False)
    adj_people = Column(TINYINT(4), nullable=False)
    adj_tier = Column(TINYINT(4), nullable=False)
    challenge_desc = Column(String(80), nullable=False)
    winner_desc = Column(String(80), nullable=False, server_default=text("'--'"))
    mob_name = Column(String(30), nullable=False)
    is_active = Column(TINYINT(1), nullable=False, server_default=text("0"))

    @property
    def is_completed(self):
        """Boolean whether challenge is completed"""
        if self.winner_desc != '' and self.winner_desc != "'--'":
            return True
        return False

    @property
    def display_tier(self):
        """Display challenge tier"""
        tiers = {
            1: 'F', 2: 'D', 3: 'C',
            4: 'B', 5: 'A', 6: 'S',
            7: 'SS', 8: 'SS', 9: 'SS'
        }
        return (f'{tiers[self.adj_tier]} ({tiers[self.orig_tier]})')

    def __repr__(self):
        return (f'<Challenge> "{self.mob_name}" ({self.challenge_id}) / '
                f'Active: {self.is_active} / Tier: "{self.display_tier}" / '
                f'Winner: "{self.winner_desc}"')
