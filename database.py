"""Database connection"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from .database_secret import URL, ECHO

engine = create_engine(
    url=URL,
    echo=ECHO,
    pool_pre_ping=True
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata
