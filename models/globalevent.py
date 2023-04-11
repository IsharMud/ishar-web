"""Database classes/models"""
from datetime import datetime
from functools import cached_property

from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT

from delta import stringify
from database import Base


class GlobalEvent(Base):
    """Global events within the game, which provide bonuses"""
    __tablename__ = 'global_event'

    event_type = Column(TINYINT(4), primary_key=True, unique=True)
    start_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    end_time = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    event_name = Column(String(20), nullable=False)
    event_desc = Column(String(40), nullable=False)
    xp_bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    shop_bonus = Column(TINYINT(4), nullable=False, server_default=text("0"))
    celestial_luck = Column(TINYINT(1), nullable=False, server_default=text("0"))

    @property
    def start(self):
        """Stringified approximate timedelta since event start"""
        return stringify(datetime.utcnow() - self.start_time)

    @property
    def end(self):
        """Stringified approximate timedelta until event end"""
        return stringify(self.end_time - datetime.utcnow())

    @cached_property
    def display_name(self):
        """Formatted name of the event"""
        return self.event_name.replace('_', ' ').title()

    @cached_property
    def display_string(self):
        """Formatted full display string for the event,
            with display name, and any event_desc from database"""
        out = self.display_name
        if self.event_desc and self.event_desc != '':
            out += f' -- {self.event_desc}'
        return out

    @cached_property
    def is_luck(self):
        """Boolean based upon celestial_luck from database"""
        if self.celestial_luck == 1:
            return True
        return False

    def __repr__(self):
        return ('<GlobalEvent> / '
                f'Type: "{self.event_type}" / '
                f'Name: "{self.event_name}" ("{self.display_name}") / '
                f'Desc: "{self.event_desc}" / '
                f'Start: "{self.start_time}" ("{self.start}") / '
                f'End: "{self.end_time}" ("{self.end}")')
