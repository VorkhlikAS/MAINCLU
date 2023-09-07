from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User

async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.id.desc()))
    return result.scalars().all()

async def get_user_status(session: AsyncSession, id: int) -> int:
    result = await session.execute(select(User.status).where(User.id == id))
    return result.scalars().first()

async def set_user_status(session: AsyncSession, id:int, new_status: int):
    new_status = await session.execute(
        update(User)
        .where(User.id == id)
        .values({"status": new_status})
    )

def add_user(session: AsyncSession, id:int, name: str, status: int):
    new_user = User(id=id, name=name, status=status)
    session.add(new_user)
    return new_user