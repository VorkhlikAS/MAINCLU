import os
import requests
import telebot
from telebot import types


BOT_TOKEN = os.environ.get('BOT_TOKEN')
BACKEND_URL = os.environ.get('BACKEND_URL')
 
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    if message.text == '/start':
        # Сохраним пользователя в БД
        try:
            response = get_status(message.from_user.id)
            if response.status_code == 404:
                response = requests.post(f"{BACKEND_URL}/users/", 
                    json={
                        "id": f"{message.from_user.id}",
                        "name": f"{message.from_user.username}",
                        "status": 0
                        },)
                #     headers={"Content-Type": "application/json"}
                # )
        except Exception as e:
            bot.send_message(message.from_user.id, f'{e}')
        # Приветствие
        # bot.send_photo(message.from_user.id, 'https://cs14.pikabu.ru/post_img/2022/11/03/11/1667504777134725533.jpg')
        bot.send_video(message.from_user.id, 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNW8yNThheTYxdHF2YXpseDVjd2w4aGZ4amQ1Z3hhbm5iNGk5cGQwbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/VFf2015gPpE80ii9iX/giphy.gif', None, 'Text')
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='DEBUG: Все пользователи', callback_data='all_users')
        keyboard.add(btn)
        btn = types.InlineKeyboardButton(text='DEBUG: Мой статус', callback_data='my_status')
        keyboard.add(btn)
        btn = types.InlineKeyboardButton(text='Speech2Speech', callback_data='s2s')
        keyboard.add(btn)
        btn = types.InlineKeyboardButton(text='Speech2Text', callback_data='s2t')
        keyboard.add(btn)
        bot.send_message(message.from_user.id, "MAINCLU это приложение для распознования речи с особенностями!\n"
                                        "\n"
                                        "***\n",
                                        reply_markup=keyboard)


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "all_users":
        try:
            response = requests.get(f"{BACKEND_URL}/users/get")
            bot.send_message(call.from_user.id, response)
        except Exception as e:    
            bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')
    elif call.data == "my_status":
        try: 
            response = get_status(call.from_user.id)
            bot.send_message(call.from_user.id, response)
        except Exception as e:
            bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')
    elif call.data == "s2s":
        try: 
            set_user_status(call, 1)
            bot.send_message(call.from_user.id, "Включен режим перевода в Голос")
            bot.send_message(call.from_user.id, "Ожидаю ваше сообщение...")
        except Exception as e:
            bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')    
    elif call.data == "s2t":
        try: 
            set_user_status(call, 2)
            bot.send_message(call.from_user.id, "Включен режим перевода в Текст")
            bot.send_message(call.from_user.id, "Ожидаю ваше сообщение...")
        except Exception as e:
            bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')    


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    response = get_status(message.from_user.id)
    status = response.json()['status']
    
    if status in (1, 2):
        
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        files = {
            'voice': downloaded_file,
        }

        response = requests.post(f'{BACKEND_URL}/voice/', files=files, params={
            "user_id": message.from_user.id,
            "user_status": status
        })
        if status == 1:
            bot.send_voice(message.from_user.id, response.content, reply_to_message_id=message)
        else: 
            bot.reply_to(message, response.json()['result'])
    else:
        bot.reply_to(message, "Выберите вид обработки")
        

def set_user_status(call: int, status: int) -> None: 
    try: 
        requests.post(f"{BACKEND_URL}/users/status/", # TODO: replace with params
                                json={
                                    "id":f"{call.from_user.id}",
                                    "status": status
                                },)
    except Exception as e: 
        bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')


def get_status(user_id: int) -> requests.Response:
    response = requests.get(f"{BACKEND_URL}/users/status/get", 
                            params={
                                "user_id": user_id,
                                },) 
    return response


bot.infinity_polling()
