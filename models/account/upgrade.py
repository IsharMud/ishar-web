"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT
from sqlalchemy.orm import relationship

from database import Base


class AccountUpgrade(Base):
    """Upgrades that are available to accounts"""
    __tablename__ = 'account_upgrades'

    id = Column(TINYINT(4), primary_key=True)
    cost = Column(MEDIUMINT(4), nullable=False)
    description = Column(String(200), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    max_value = Column(MEDIUMINT(4), nullable=False, server_default=text("1"))
    scale = Column(TINYINT(4), nullable=False, server_default=text("1"))
    is_disabled = Column(TINYINT(1), nullable=False, server_default=text("0"))

    def __repr__(self):
        return (f'<AccountUpgrade> "{self.name}" ({self.id}) / '
                f'Cost: {self.cost} / Max: {self.max_value}')


class AccountsUpgrade(Base):
    """Account upgrade associated with account, and the level of upgrade"""
    __tablename__ = 'accounts_account_upgrades'

    account_upgrades_id = Column(ForeignKey('account_upgrades.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    amount = Column(MEDIUMINT(4), nullable=False)

    account = relationship('Account', back_populates='upgrades')
    upgrade = relationship('AccountUpgrade')

    def __repr__(self):
        return (f'<AccountsUpgrade> {self.upgrade} : {self.amount} @ '
                f'{self.account}')
