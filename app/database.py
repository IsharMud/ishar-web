import database_secret
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine      = create_engine(database_secret.sql_uri, echo=True)
db_session  = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base        = declarative_base()
Base.query  = db_session.query_property()

