import random
import telebot
from  telebot import types
import time

bot = telebot.TeleBot('6682494061:AAFLZH7Qj32HYffI2UQdgpXxj0giooBe5iQ')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start": #запрашивает начало боя
        #global enemy1
        #global player1
        #enemy1 = Npc(hp=10, kz=10, kz_flag=0, attack_flag=0)
        #player1 = Player(hp=20, kz=14, kz_flag=0, hillC=1, attack_flag=0)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='В бой', callback_data='first_room')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='В бой', callback_data='fight_loop')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='В бой', callback_data='fight_loop')
        keyboard.add(key_oven)
        bot.send_message(message.from_user.id, text='в бой?', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Если хотите начать игру, то напишите '/start'.")