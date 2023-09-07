import uvicorn
from fastapi import FastAPI, HTTPException
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
    id: int
    name: str
    status: int
    
    
class UserIdSchema(BaseModel):
    id: int
    
    
class UserStatusSchema(BaseModel):
    id: int
    status: int


@app.get("/users/get", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await service.get_users(session)
    return [UserSchema(id=c.id, name=c.name, status=c.status) for c in users]   


@app.get("/score/get")
async def root():
    return {"score": 100}


@app.post("/users/status/get")
async def get_status(user: UserIdSchema, session: AsyncSession = Depends(get_session)):
    user_status = await service.get_user_status(session, user.id)
    if user_status is None:
        raise HTTPException(status_code=404, detail="Invalid user id")
    else: 
        return UserStatusSchema(id=user.id, status=user_status)   
    
@app.post("/users/status/")
async def get_status(user: UserStatusSchema, session: AsyncSession = Depends(get_session)):
    await service.set_user_status(session, user.id, user.status)
    return user  


@app.post("/users/")
async def add_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    user = service.add_user(session, user.id, user.name, user.status)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        # raise exceptions.DuplicatedEntryError("The user is already stored")
        raise HTTPException(status_code=404, detail="User already exists")
        # return 0


if __name__ == "__main__":
    init_models()
    uvicorn.run(app, host='0.0.0.0')
