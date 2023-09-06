from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User

async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.id.desc()))
    return result.scalars().all()


def add_user(session: AsyncSession, name: str, population: int):
    new_user = City(name=name, population=population)
    session.add(new_user)
    return new_user