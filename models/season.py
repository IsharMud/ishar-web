"""Database classes/models"""
from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from delta import stringify
from database import Base


class Season(Base):
    """Details of the start and end times of in-game cyclical seasons"""
    __tablename__ = 'seasons'

    season_id = Column(INTEGER(11), primary_key=True)
    is_active = Column(TINYINT(4), nullable=False)
    effective_date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    expiration_date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))

    @property
    def effective(self):
        """Stringified approximate timedelta since season started"""
        return stringify(datetime.utcnow() - self.effective_date)

    @property
    def expires(self):
        """Stringified approximate timedelta until season ends"""
        return stringify(self.expiration_date - datetime.utcnow())

    def __repr__(self):
        return (f'<Season> {self.season_id} / Active: {self.is_active} / '
                f'{self.effective_date} ({self.effective}) - '
                f'{self.expiration_date} ({self.expires})')
