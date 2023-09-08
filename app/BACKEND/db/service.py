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
        .values(status=new_status)
    )
    result = await session.execute(select(User.status).where(User.id == id))
    print(result.scalars().first())
    session.commit()
    
    # if db_user is None:
    #     return None

    # # Update model class variable from requested fields 
    # for var, value in vars(user).items():
    #     setattr(db_user, var, value) if value else None

    # db_user.modified = modified_now
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user
    # session.execute(
    #     update(User),
    #         [
    #             {"id": id, "status": new_status},
    #         ],
    # )
    # session.commit()


def add_user(session: AsyncSession, id:int, name: str, status: int):
    new_user = User(id=id, name=name, status=status)
    session.add(new_user)
    # session.refresh()
    session.commit()
    session.flush()
    return new_user