import uvicorn
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from fastapi_async_sqlalchemy import exceptions
from db import service
from db import base, get_session
from db.manager import init_models

app = FastAPI()


class UserSchema(BaseModel):
    name: str
    status: int


@app.get("/users/get", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await service.get_users(session)
    return [UserSchema(name=c.name, status=c.status) for c in users]   


@app.post("/users/")
async def add_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    user = service.add_user(session, user.name, user.status)
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

if __name__ == "__main__":
    init_models()
    uvicorn.run(app, host='0.0.0.0')
