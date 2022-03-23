# from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
#
# from src.config import settings
from src.app.base.model_base import BaseModel
#
# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(cls=BaseModel)
