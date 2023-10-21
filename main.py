import random
import telebot
from  telebot import types


def fightRound2pl():
    # while player1.hp>0 or
    pass

def fightRound3pl():
    pass
class Player():
    def __init__(self,hp, kz, kz_flag, hillC):
        self.hp = hp
        self.kz = kz
        self.kz_flag = kz_flag
        self.hillC = hillC
        self.kz_flag = 0
    def attack(self):
        if self.kz-random.randint(1,20)>=0:
            self.hp -= random.randint(1,8)

    def defence(self):
        self.kz+=3
        self.kz_flag = 1
    def defenceoff(self):
        self.kz -= 3
        self.kz_flag = 0

    def hill(self):
        pass

class Npc():
    def __init__(self,hp, kz, kz_flag):
        self.hp = hp
        self.kz = kz
        self.kz_flag = kz_flag

        self.kz_flag = 0

    def attack(self):
        if self.kz-random.randint(1,20)>=0:
            self.hp -= random.randint(1,8)

    def defence(self):
        self.kz += 3
        self.kz_flag = 1

    def defenceoff(self):
        self.kz -= 3
        self.kz_flag = 0

player1 = Player(hp=20, kz=14, kz_flag=0, hillC=0)
enemy1 = Npc(hp=10, kz=10,kz_flag=0)
print(player1.hp)

bot = telebot.TeleBot('6682494061:AAFLZH7Qj32HYffI2UQdgpXxj0giooBe5iQ')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start": #запрашивает начало боя
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='В бой', callback_data='fight_loop')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='В бой', callback_data='fight_loop')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='В бой', callback_data='fight_loop')
        keyboard.add(key_oven)
        bot.send_message(message.from_user.id, text='в бой?', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши /start")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "fight_loop": # запускает круг боя(условия выхода пока нет)
        msg = "text"
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='защита', callback_data='defence_b')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, "выберите действие", reply_markup=keyboard)
        print("inside fight")
    elif call.data == "attack_b": # делает атаку по enemy1(надо прописать атаку по игроку)
        enemy1.attack()
        # bot.send_message(call.message.chat.id, "у enemy1 осталось "+str(enemy1.hp)+" hp")
        #атака по игроку(или оборона)
        player1.attack()
        aaa="у enemy1 осталось "+str(enemy1.hp)+" hp\n"+"enemy1 нанёс вам урон, ваш текущий hp "+str(player1.hp)
        bot.send_message(call.message.chat.id,text=aaa)


        print("inside attack")
    elif call.data == "defence_b":
        print("inside defence")







bot.polling(none_stop=True, interval=0)




