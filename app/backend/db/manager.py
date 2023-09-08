from sqlalchemy.ext.asyncio import AsyncSession

from db.base import sync_engine, Base, async_session, SYNC_DATABASE
from sqlalchemy_utils import create_database, database_exists


def init_models():
    if not database_exists(SYNC_DATABASE):
        create_database(SYNC_DATABASE)
    Base.metadata.create_all(bind=sync_engine)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
