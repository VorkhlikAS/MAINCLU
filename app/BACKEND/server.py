from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from fastapi_async_sqlalchemy import exceptions
from db import service
from db import base


app = FastAPI()


class UserSchema(BaseModel):
    name: str
    state: int


@app.get("/users/get", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(base.get_session)):
    users = await service.get_users(session)
    return [UserSchema(name=c.name, state=c.state) for c in users]   


@app.post("/users/")
async def add_user(user: UserSchema, session: AsyncSession = Depends(base.get_session)):
    user = service.add_user(session, user.name, user.state)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise exceptions.DuplicatedEntryError("The user is already stored")
        # return 0


@app.get("/SCORE/GET")
async def root():
    return {"score": 100}
