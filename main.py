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
        if (self.kz-random.randint(1,21))<=0:
            self.hp -= random.randint(1,8)

    def defence(self):
        self.kz+=2
        self.kz_flag = 1
    def defenceoff(self):
        if self.kz_flag == 1:
            self.kz -= 2
        self.kz_flag = 0

    def hill(self):
        if self.hillC > 0:
            self.hp += random.randint(1,6)
            self.hillC -= 1

class Npc():
    def __init__(self,hp, kz, kz_flag):
        self.hp = hp
        self.kz = kz
        self.kz_flag = kz_flag

        self.kz_flag = 0

    def attack(self):
        if (self.kz-random.randint(1,21))<=0:
            self.hp -= random.randint(1,8)

    def defence(self):
        self.kz += 5
        self.kz_flag = 1

    def defenceoff(self):
        self.kz -= 5
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
        global enemy1
        enemy1 = Npc(hp=10, kz=10, kz_flag=0)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='лёгкая атака и блок', callback_data='defence_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='выпить зелье лечения (осталось'+str(player1.hillC)+')', callback_data='defence_b')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, "выберите действие", reply_markup=keyboard)
        print("inside fight")

    elif call.data == "attack_b": # делает атаку по enemy1(надо прописать атаку по игроку)
        player1.defenceoff()
        enemy1.attack()
        # bot.send_message(call.message.chat.id, "у enemy1 осталось "+str(enemy1.hp)+" hp")
        #атака по игроку(или оборона)
        player1.attack()
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='лёгкая атака и блок', callback_data='defence_b')
        keyboard.add(key_oven)
        aaa="у enemy1 осталось "+str(enemy1.hp)
        bbb = "enemy1 бьёт вас, ваш текущий hp " + str(player1.hp)
        bot.send_message(call.message.chat.id, text=aaa)
        bot.send_message(call.message.chat.id,text=bbb, reply_markup=keyboard)
        print("inside attack")

    elif call.data == "defence_b":
        player1.defenceoff()
        print("inside defence")
        player1.defence()
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='лёгкая атака и блок', callback_data='defence_b')
        keyboard.add(key_oven)
        player1.attack()
        enemy1.hp -= 2
        print(player1.kz)
        aaa = "вы соверщаете лёгкую атаку и делаете блок, enemy1 hp = "+str(enemy1.hp)
        bbb = "enemy1 бьёт вас, ваш текущий hp " + str(player1.hp)
        bot.send_message(call.message.chat.id, text=aaa)
        bot.send_message(call.message.chat.id, text=bbb, reply_markup=keyboard)
    elif call.data == "hill":
        pass







bot.polling(none_stop=True, interval=0)




