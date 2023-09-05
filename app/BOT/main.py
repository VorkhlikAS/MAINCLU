import os
import requests
import telebot
from telebot import types


BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    # bot.reply_to(message, "Howdy, how are you doing?")
    if message.text == '/start':
        # Приветствие
        bot.send_photo(message.from_user.id, 'https://cs14.pikabu.ru/post_img/2022/11/03/11/1667504777134725533.jpg')
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Секретная кнопка', callback_data='secret_btn')
        keyboard.add(btn)
        bot.send_message(message.from_user.id, "Привет, вас приветствует тестовая версия приложения корректора речи MANUL!\n"
                                        "Данный бот предназначен для анализа речи пользователя, оценки дефектов и предоставления упражнений для профилактики этих дефектов\n"
                                        "***\n"
                                        "Попробуйте отправить голосовое сообщение для оценки качества речи.\n"
                                        "***\n",
                                        reply_markup=keyboard)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    response = requests.get("http://manul-backend:8000/SCORE/GET")
    bot.reply_to(message, response)

bot.infinity_polling()
