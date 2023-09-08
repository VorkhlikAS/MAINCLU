import uvicorn
# import aiofiles
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from fastapi_async_sqlalchemy import exceptions
from db import service
from db import base, get_session
from db.manager import init_models
from data import ModelWorker
from fastapi.responses import FileResponse
import os
import time

app = FastAPI()
model = ModelWorker()

class UserSchema(BaseModel):
    id: int
    name: str
    status: int
    
    
class UserStatusSchema(BaseModel):
    id: int
    status: int


@app.get("/users/get", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await service.get_users(session)
    return [UserSchema(id=c.id, name=c.name, status=c.status) for c in users]   


@app.post("/voice/")
async def upload_voice(voice: UploadFile, user_id: int, user_status: int):
    filename = f'{user_id}_{time.time()}.ogg'
    # out_file_path = os.path.join(os.getcwd(), os.path.join('data', filename))
    
    # async with aiofiles.open(out_file_path, 'wb') as out_file:
    #     content = await voice.read()  # async read
    #     await out_file.write(content)  # async write
    
    result = await model.run_model(voice, filename, user_status)
        
    if user_status == 1:
        return FileResponse(result)
    else:
        return { "result": result }


@app.get("/users/status/get")
async def get_status(user_id: int, session: AsyncSession = Depends(get_session)):
    user_status = await service.get_user_status(session, user_id)
    if user_status is None:
        raise HTTPException(status_code=404, detail="Invalid user id")
    else: 
        return UserStatusSchema(id=user_id, status=user_status)   
    
@app.post("/users/status/")
async def set_status(user: UserStatusSchema, session: AsyncSession = Depends(get_session)):
    await service.set_user_status(session, user.id, user.status)
    return user  


@app.post("/users/")
async def add_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    user = await service.add_user(session, user.id, user.name, user.status)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        # raise exceptions.DuplicatedEntryError("The user is already stored")
        raise HTTPException(status_code=404, detail="User already exists")
        # return 0
    


if __name__ == "__main__":
    init_models()
    uvicorn.run(app, host='0.0.0.0')
