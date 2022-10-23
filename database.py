"""Database connection"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import database_secret

engine  = create_engine(
            url             = database_secret.URL,
            echo            = database_secret.ECHO,
            pool_pre_ping   = True
        )

db_session  = scoped_session(
                sessionmaker(
                    autocommit  = False,
                    autoflush   = False,
                    bind        = engine
                )
            )

Base        = declarative_base()
Base.query  = db_session.query_property()
metadata    = Base.metadata
