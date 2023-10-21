import random
import telebot
from  telebot import types
import time


players_hard_attack_pack = ["Вы совершаете точный удар своим кинжалом!", "Замахнувшись кинжалом, вы совершаете сильную атаку кинжалом!", "Замахнувшись кинжалом, вы резко меняете направление удара и бьете!", "Cовершив бесстрашный выпад, вы бросаетесь на противника с атакой!", "Метко, как стрела, ваш кинжал находит уязвимое место противника!"]
enemy_attack_pack = ["Скелет махнул мечом в вашем направлении!", "Скелет проводит неуклюжий, но сильный удар своим коротким мечом!", "Ржавый меч скелета возвышается над вами, угрожая пронзить вас!", "Скелет с мечом движется с мрачной решимостью, стремясь поразить вас!", "Вы чувствуете холодное дыхание смерти, когда скелет поднимает свой меч и наносит атаку!"]
players_safe_attack_pack = ["Вы с утонченной ловкостью проводите атаку, сохраняя одновременно защиту!", "С мастерством фехтования, вы проворачиваете атаку в моменте защиты!", "Ваш кинжал двигается, как танцор, на грани атаки и защиты!", "Аккуратная атака с кинжалом укрепляет вашу защиту, не оставляя уязвимых точек!", "Вы умело комбинируете атаку с защитой, ограничивая контратаку противника!"]
players_hill_pack = ["Вы выпиваете зелье лечения, ощущая, как сила и энергия восполняются в ваших жилах!", "После глотка зелья, вы чувствуете, как раны заживают и вы становитесь сильнее!", "Вы быстро выпиваете красную жидкость, чувствуя, как теплое облегчение распространяется внутри вас!", "Вы пьете зелье лечения, и тут же ощущаете, как силы возвращаются!"]



def fightRound2pl():
    # while player1.hp>0 or
    pass

def fightRound3pl():
    pass
class Player():
    def __init__(self,hp, kz, kz_flag, hillC, attack_flag):
        self.hp = hp
        self.kz = kz
        self.kz_flag = kz_flag
        self.hillC = hillC
        self.kz_flag = 0
        self.attack_flag = attack_flag
    def attack(self):
        self.attack_flag = 0
        r = (self.kz - random.randint(1, 21))
        if r <= 0:
            self.hp -= random.randint(1, 8)
            self.attack_flag = 1

    def defence(self):
        self.kz+=2
        self.kz_flag = 1
    def defenceoff(self):
        if self.kz_flag == 1:
            self.kz -= 2
        self.kz_flag = 0

    def hill(self):
        if self.hillC > 0:
            self.hp += random.randint(2,7)
            self.hillC -= 1

class Npc():
    def __init__(self,hp, kz, kz_flag, attack_flag):
        self.hp = hp
        self.kz = kz
        self.kz_flag = kz_flag
        self.kz_flag = 0
        self.attack_flag = attack_flag

    def attack(self):
        self.attack_flag = 0
        r = (self.kz-random.randint(1,21))
        if r <= 0:
            self.hp -= random.randint(1,8)
            self.attack_flag = 1

    def defence(self):
        self.kz += 5
        self.kz_flag = 1

    def defenceoff(self):
        self.kz -= 5
        self.kz_flag = 0

player1 = Player(hp=20, kz=14, kz_flag=0, hillC=1, attack_flag=0)
enemy1 = Npc(hp=10, kz=10,kz_flag=0, attack_flag=0)
print(player1.hp)

bot = telebot.TeleBot('6682494061:AAFLZH7Qj32HYffI2UQdgpXxj0giooBe5iQ')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start": #запрашивает начало боя
        global enemy1
        global player1
        enemy1 = Npc(hp=10, kz=10, kz_flag=0, attack_flag=0)
        player1 = Player(hp=20, kz=14, kz_flag=0, hillC=1, attack_flag=0)
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
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось '+str(player1.hillC)+')', callback_data='hill')
        keyboard.add(key_oven)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)
        print("inside fight")

    elif call.data == "attack_b": # делает атаку по enemy1(надо прописать атаку по игроку)
        player1.defenceoff()
        enemy1.attack()
        #атака по игроку(или оборона)
        player1.attack()
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')',callback_data='hill')
        keyboard.add(key_oven)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text=random.choice(players_hard_attack_pack))
        time.sleep(0.7)
        if enemy1.attack_flag:
            bot.send_message(call.message.chat.id, text="Вы попадаете по скелету!")
        else:
            bot.send_message(call.message.chat.id, text="Но вы не попадаете по скелету.")
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text=random.choice(enemy_attack_pack))
        time.sleep(0.7)
        if player1.attack_flag:
            bot.send_message(call.message.chat.id, text="Скелет попадает по вам!")
        else:
            bot.send_message(call.message.chat.id, text="Но скелет не попадает по вам!")
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text="Ваш HP: "+str(player1.hp)+" HP\nHP скелета: "+str(enemy1.hp)+" HP", reply_markup=keyboard)
        print("inside attack")

    elif call.data == "defence_b":
        player1.defenceoff()
        print("inside defence")
        player1.defence()
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')', callback_data='hill')
        keyboard.add(key_oven)
        player1.attack()
        enemy1.hp -= 2
        print(player1.kz)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text=random.choice(players_safe_attack_pack))
        time.sleep(0.7)
        if enemy1.attack_flag:
            bot.send_message(call.message.chat.id, text="Вы попадаете по скелету и готовы отражать его атаку!")
        else:
            bot.send_message(call.message.chat.id, text="Вы не попадаете по скелету, но пытаетесь отразить от его атаки.")
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text=random.choice(enemy_attack_pack))
        time.sleep(0.7)
        if player1.attack_flag:
            bot.send_message(call.message.chat.id, text="Скелет попадает по вам!")
        else:
            bot.send_message(call.message.chat.id, text="Но скелет не попадает по вам!")
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text="Ваш HP: "+str(player1.hp)+" HP\nHP скелета: "+str(enemy1.hp)+" HP", reply_markup=keyboard)

    elif call.data == "hill":
        if player1.hillC > 0 and player1.hp < 20:
            plhp = player1.hp
            player1.hill()
            if player1.hp > 20:
                player1.hp = 20
            player1.defenceoff()
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')',callback_data='hill')
            keyboard.add(key_oven)
            player1.attack()
            player1.hill()
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
            time.sleep(0.7)
            bot.send_message(call.message.chat.id, text=random.choice(players_hill_pack))
            time.sleep(0.7)
            bot.send_message(call.message.chat.id, text=random.choice(enemy_attack_pack))
            time.sleep(0.7)
            bot.send_message(call.message.chat.id, text=f"Вы восстановили {plhp} HP!")
            time.sleep(0.7)
            if player1.attack_flag:
                bot.send_message(call.message.chat.id, text="Скелет попадает по вам!")
            else:
                bot.send_message(call.message.chat.id, text="Но скелет не попадает по вам!")
            bot.send_message(call.message.chat.id, text="Ваш HP: "+str(player1.hp)+" HP\nHP скелета: "+str(enemy1.hp)+" HP", reply_markup=keyboard)
        if player1.hp == 20:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
            time.sleep(0.7)
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')',callback_data='hill')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id, text="Вы и так полностью здоровы.", reply_markup=keyboard)
        else:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            time.sleep(0.7)
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')', callback_data='hill')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id, text="У вас кончились зелья лечения!", reply_markup=keyboard)














bot.polling(none_stop=True, interval=0)




