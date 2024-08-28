from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase

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
    engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
