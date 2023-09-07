import os
import requests
import telebot
from telebot import types


BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    if message.text == '/start':
        # Сохраним пользователя в БД
        try:
            response = get_status(message.from_user.id)
            if response.status_code == 404:
                response = requests.post("http://manul-backend:8000/users/", 
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
        bot.send_photo(message.from_user.id, 'https://cs14.pikabu.ru/post_img/2022/11/03/11/1667504777134725533.jpg')
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='DEBUG: Все пользователи', callback_data='all_users')
        keyboard.add(btn)
        btn = types.InlineKeyboardButton(text='DEBUG: Мой статус', callback_data='my_status')
        keyboard.add(btn)
        btn = types.InlineKeyboardButton(text='Speech2Speech', callback_data='s2s')
        keyboard.add(btn)
        btn = types.InlineKeyboardButton(text='Voice2Text', callback_data='s2t')
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
            response = requests.get("http://manul-backend:8000/users/get")
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
            bot.send_message(call.from_user.id, "Ожидаю ваше сообщение...")
        except Exception as e:
            bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')    
    elif call.data == "s2t":
        try: 
            set_user_status(call, 2)
            bot.send_message(call.from_user.id, "Ожидаю ваше сообщение...")
        except Exception as e:
            bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')    


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    response = get_status(message.from_user.id)
    bot.reply_to(message, response.json())
    if response.json()['status'] in (1, 2):
        bot.reply_to(message, "Бла бла бла, ничего не понимаю")
    
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    # try:
    #     response = requests.get("http://manul-backend:8000/SCORE/GET")
    #     bot.reply_to(message, response)
    # except Exception as e:    
    #     bot.reply_to(message, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')
        

def set_user_status(call: int, status: int) -> None: 
    try: 
        requests.post("http://manul-backend:8000/users/status/",
                                json={
                                    "id":f"{call.from_user.id}",
                                    "status": status
                                })
    except Exception as e: 
        bot.send_message(call.from_user.id, f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')


def get_status(user_id: int) -> requests.Response:
    response = requests.post("http://manul-backend:8000/users/status/get", 
                            json={
                                "id": f"{user_id}",
                                },) 
    return response


bot.infinity_polling()
