
"""Database classes/models"""
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from database import Base, metadata


class News(Base):
    """News posts for the front page of the website"""
    __tablename__ = 'news'

    news_id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    subject = Column(String(64), nullable=False, server_default=text("''"))
    body = Column(Text, nullable=False)

    account = relationship(
        'Account',
        single_parent=True,
        uselist=False
    )

    def __repr__(self):
        return (f'<News> "{self.subject}" ({self.news_id}) @ '
                f'{self.created_at} by {self.account}')
