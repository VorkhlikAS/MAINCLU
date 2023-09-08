import os
import shutil
import aiofiles


DATAPATH = os.path.join(os.getcwd(), 'data')

class ModelWorker:
    
    def __init__(self, ):
        # TODO: Добавить открытие моделей
        pass
    
    async def run_model(self, file: any, filename: str, status: int):
        # TODO: Добавить обработку голосового сообщения пользователя
        # ...
        filepath = os.path.join(DATAPATH, os.path.join('input', filename)) # Сохраняет записи для дальнейшего использования
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
            
        tgr_filepath = os.path.join(DATAPATH, os.path.join('output', filename))
        shutil.copyfile(filepath, tgr_filepath) # TODO: Заменить на генерацию файла моделью

        if status == 1:
            return tgr_filepath
        else: 
            return "[WIP]: Your speech translated"
        