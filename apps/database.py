from sqlalchemy import NullPool
from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

if settings.MODE == 'TEST':
    database_params = {"poolclass": NullPool}
    database_url = settings.TEST_DB_URL
else:
    database_params = {}
    database_url = settings.DB_URL

engine = create_async_engine(
    database_url, **database_params
)
async_session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
