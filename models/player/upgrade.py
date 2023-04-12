"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT
from sqlalchemy.orm import relationship

from database import Base


class PlayerRemortUpgrade(Base):
    """Remort upgrades that player characters have"""
    __tablename__ = 'player_remort_upgrades'

    upgrade_id = Column(ForeignKey('remort_upgrades.upgrade_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    player_id = Column(ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    value = Column(INTEGER(11), nullable=False)
    essence_perk = Column(TINYINT(1), nullable=False, server_default=text("0"))

    player = relationship('Player', backref='remort_upgrades')
    remort_upgrade = relationship('RemortUpgrade')

    def __repr__(self):
        return (f'<PlayerRemortUpgrade> "{self.remort_upgrade}" '
                f'({self.upgrade_id}) : {self.value} ({self.essence_perk}) @ '
                f'{self.player}')


class RemortUpgrade(Base):
    """Remort upgrades that are available to player characters"""
    __tablename__ = 'remort_upgrades'

    upgrade_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False, unique=True, server_default=text("''"))
    renown_cost = Column(SMALLINT(6), nullable=False)
    max_value = Column(SMALLINT(6), nullable=False)
    scale = Column(TINYINT(4), nullable=False, server_default=text("10"))
    display_name = Column(String(30), nullable=False)
    can_buy = Column(TINYINT(1), nullable=False, server_default=text("1"))
    bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    survival_scale = Column(TINYINT(4), nullable=False)
    survival_renown_cost = Column(TINYINT(4), nullable=False)

    def __repr__(self):
        return (f'<RemortUpgrade> "{self.display_name}" ({self.upgrade_id})')
