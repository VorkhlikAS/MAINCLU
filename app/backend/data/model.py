import os
import shutil
import aiofiles
import speech_recognition as sr
import soundfile as sf
from gtts import gTTS


DATAPATH = os.path.join(os.getcwd(), 'data')

class ModelWorker:
    
    def __init__(self, ):
        # TODO: Добавить открытие моделей
        self.r= sr.Recognizer()
        self.lang = 'ru'
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

        data, samplerate = sf.read(filepath)
        filepath = os.path.join(DATAPATH, os.path.join('input', filename.replace('ogg', 'wav')))
        sf.write(filepath, data, samplerate)
        with sr.AudioFile(filepath) as source:
            # listen for the data (load audio to memory)
            audio_data = self.r.record(source)
            # recognize (convert from speech to text)
            text = self.r.recognize_google(audio_data, language='ru-RU')
    
        if status == 1:
            voice = gTTS(text=text, lang=self.lang, slow=False)
            voice.save(tgr_filepath)
            return tgr_filepath
        else: 
            return text
        