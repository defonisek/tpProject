import random
import telebot
from  telebot import types
import time


players_hard_attack_pack = ["Вы совершаете точный удар своим кинжалом!", "Замахнувшись кинжалом, вы совершаете сильную атаку кинжалом!", "Замахнувшись кинжалом, вы резко меняете направление удара и бьете!", "Cовершив бесстрашный выпад, вы бросаетесь на противника с атакой!", "Метко, как стрела, ваш кинжал находит уязвимое место противника!"]
enemy_attack_pack = ["Скелет махнул мечом в вашем направлении!", "Скелет проводит неуклюжий, но сильный удар своим коротким мечом!", "Ржавый меч скелета возвышается над вами, угрожая пронзить вас!", "Скелет с мечом движется с мрачной решимостью, стремясь поразить вас!", "Вы чувствуете холодное дыхание смерти, когда скелет поднимает свой меч и наносит атаку!"]
players_safe_attack_pack = ["Вы с утонченной ловкостью проводите атаку, сохраняя одновременно защиту!", "С мастерством фехтования, вы проворачиваете атаку в моменте защиты!", "Ваш кинжал двигается, как танцор, на грани атаки и защиты!", "Аккуратная атака с кинжалом укрепляет вашу защиту, не оставляя уязвимых точек!", "Вы умело комбинируете атаку с защитой, ограничивая контратаку противника!"]
players_hill_pack = ["Вы выпиваете зелье лечения, ощущая, как сила и энергия восполняются в ваших жилах!", "После глотка зелья, вы чувствуете, как раны заживают и вы становитесь сильнее!", "Вы быстро выпиваете красную жидкость, чувствуя, как теплое облегчение распространяется внутри вас!", "Вы пьете зелье лечения, и тут же ощущаете, как силы возвращаются!"]




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
        if player1.hp > 20:
            player1.hp = 20

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

player1 = Player(hp=2, kz=14, kz_flag=0, hillC=1, attack_flag=0)
enemy1 = Npc(hp=10, kz=10,kz_flag=0, attack_flag=0)
flags = {'first_room_searched':0,'torch_acq':0,'first_key_acq':0,'stupid':0,'skeleton_fight':0}

bot = telebot.TeleBot('6682494061:AAFLZH7Qj32HYffI2UQdgpXxj0giooBe5iQ')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        global flags
        global player1
        global enemy1
        player1 = Player(hp=2, kz=14, kz_flag=0, hillC=1, attack_flag=0) # изменять для тестирования праметры игрока
        enemy1 = Npc(hp=10, kz=10,kz_flag=0, attack_flag=0)
        flags = {'first_room_searched':0,'torch_acq':0,'first_key_acq':0,'stupid':0,'skeleton_fight':0}
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Да!', callback_data='first_room_start')
        keyboard.add(key_oven)
        bot.send_message(message.from_user.id, text='Начать игру с самого начала?', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Если хотите начать игру, то напишите '/start'.")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'first_room_start': # Первая комната.
        keyboard = types.InlineKeyboardMarkup()
        if flags['first_key_acq'] == 0:
            key_oven = types.InlineKeyboardButton(text='Подойти к закрытой двери', callback_data='closed_door_nokey')
            keyboard.add(key_oven)
        else:
            key_oven = types.InlineKeyboardButton(text='Подойти к закрытой двери',callback_data='closed_door_key')
            keyboard.add(key_oven)
        if flags['first_room_searched'] == 0:
            key_oven = types.InlineKeyboardButton(text='Осмотреть комнату повнимательнее',callback_data='useless')
            keyboard.add(key_oven)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
        if flags['torch_acq'] == 0:
            key_oven = types.InlineKeyboardButton(text='Подойти к одному из факелов',callback_data='check_torch')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id,'Вы просыпаетесь в узкой каменной комнате с сырыми стенами.'\
                        ' Холодный воздух царит в этом месте, и вам непонятно, как вы оказались здесь. Ваши воспоминания исчезли,'\
                        ' и местоположение этой комнаты остается загадкой. Окинув взглядом комнату, вы видите только две вещи, которые могут'\
                        ' заинтересовать: деревянную дверь с массивным железным замком и два старых факела, прикрепленных к стенам слева и справа'\
                        ' от вас. Осмотрев себя, вы понимаете, что вы не ранены, и в своих карманах вы находите лишь кинжал и три зелья лечения.'\
                        ' Факелы медленно горят, создавая живое пламя, бросая свои призрачные тени на стены и придавая комнате мистическую атмосферу.'\
                        ' Звук капающей воды можно услышать вдали, но источник этого звука остается неизвестным. Что вы делаете?',reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id,'Вы оглядываетесь, и перед вами все та же холодная комната, только теперь в ней висит один факел. Что вы делаете?',reply_markup=keyboard)

    elif call.data == 'useless': # Осмотр первой комнаты.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
        flags['first_room_searched'] = 1
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Вернуться в центр комнаты', callback_data='first_room_start')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,'Вы осматриваете комнату повнимательнее, но не находите ничего, кроме двух факелов и закрытой двери.',reply_markup=keyboard)
    
    elif call.data == 'closed_door_nokey': # Осмотр первой двери, если нет ключа.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Вернуться в центр комнаты',callback_data='first_room_start')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Попробовать сломать замок',callback_data='stupid')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,'Вы приближаетесь к двери и видите огромный железный замок, который не получится взломать - нечем. Вам явно понадобится ключ или какой-то другой способ открыть эту дверь.',reply_markup=keyboard)
    
    elif call.data == 'stupid': # Попытка сломать замок. 3 попытки - смерть.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
        if flags['stupid'] >= 1 and flags['stupid'] < 3:
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Перестать смотреть на свою руку',callback_data='closed_door_nokey')
            keyboard.add(key_oven)
            flags['stupid'] += 1
            bot.send_message(call.message.chat.id,text='Судя по всему, в вас проснулись мазохистские наклонности, и вы решили попробовать сломать замок еще раз. Вы поцарапались еще больше.',reply_markup=keyboard)
        elif flags['stupid'] == 3:
            bot.send_message(call.message.chat.id,text='После очередной попытки попробовать сломать замок голыми руками, ваши руки настолько истекают кровью, что вам стало плохо. Ваше зрение начало мутнеть, а ноги перестали вас держать. Вы упали и лежите на холодном полу, истекая кровью.')
            time.sleep(1)
            bot.send_message(call.message.chat.id,text='Вы погибли! Чтобы начать заново, напишите "/start".')
        else:
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Перестать смотреть на свою руку',callback_data='closed_door_nokey')
            keyboard.add(key_oven)
            flags['stupid'] += 1
            bot.send_message(call.message.chat.id,'Вы попытались сломать железный замок. Вы поцарапались. Вам больно и больше не кажется, что это была хорошая идея.',reply_markup=keyboard)

    elif call.data == 'check_torch': # Подошел к факелу.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Взять факел',callback_data='got_torch')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Отойти в центр комнаты',callback_data='first_room_start')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,text='Вы подошли к одному из двух факелов. Его пламя дает небольшое тепло. Будете подбирать?',reply_markup=keyboard)
    
    elif call.data == 'got_torch': # Взял факел. 
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
        flags['torch_acq'] = 1
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Попытаться вытащить камень',callback_data='first_key')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,text='Вы поднимаете факел и замечаете, что один из камней в стене рядом с факелом кажется подозрительным.\
                         \nЕго форма отличается от окружающих камней, и он кажется немного выдвинутым вперед.',reply_markup=keyboard)

    elif call.data == 'first_key': # Взял ключ.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=None)
        flags['first_key_acq'] = 1
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Подобрать ключ',callback_data='first_room_start')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,text='После применения небольшого усилия, камень начинает поддаваться и выпадает. Вместе с камнем на пол падает и какой-то металлический предмет. После рассмотрения предмета поближе, вы понимаете, что это - ржавый ключ.',reply_markup=keyboard)

    elif call.data == 'closed_door_key': # Открыл дверь.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Открыть замок ржавым ключом',callback_data='crossroads')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,text='Вы подошли к закрытой деревянной двери, держа факел в руке.',reply_markup=keyboard)
    
    elif call.data == 'crossroads': # Распутье.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        if flags['skeleton_fight'] == 0:
            key_oven = types.InlineKeyboardButton(text='Пойти налево',callback_data='fight_loop')
            keyboard.add(key_oven)
        else:
            key_oven = types.InlineKeyboardButton(text='Пойти налево',callback_data='dead_skeleton')
            keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Пойти направо',callback_data='fountain_door')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,text='Достав ключ из своих карманов, вы вставили его в замочную скважину. Повернув ключ, вы услышали щелчок, и замок отперся. Откинув замок в сторону, вы аккуратно проходите через дверь.'\
                        ' Вы оказываетесь в узком, холодном каменном коридоре, который тянется в обе стороны. Ваши воспоминания о прошлом остаются пустыми, и перед вами стоит выбор, который наполняет вас некоторым беспокойством. Слева от вас слышатся странные, приглушенные звуки, будто что-то движется по каменному полу.'\
                        ' Справа от вас раздаются звуки, напоминающие плеск воды.',reply_markup=keyboard)
    
    ### НИЖЕ КОД БОЯ

    elif call.data == "fight_loop": # запускает круг боя(условия выхода пока нет)
        global enemy1
        enemy1 = Npc(hp=10, kz=10, kz_flag=0, attack_flag=0) # изменять для тестирования праметры противника
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=None)
        bot.send_message(call.message.chat.id,text='Повернув влево и приближаясь к источнику странных звуков, ваше сердце начинает биться сильнее от страха и неизвестности. По мере продвижения по коридору, вы видите что-то, что быстро вызывает в вас тревожное волнение.'\
                        ' Ваш взгляд падает на живого скелета, бездумно бродящего вдоль коридора. В его руках вы видите ржавый меч. Скелет явно заметил ваше присутствие и направил свой меч в вашем направлении.',reply_markup=None)
        time.sleep(1)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось '+str(player1.hillC)+')', callback_data='hill')
        keyboard.add(key_oven)
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, "Выберите действие!", reply_markup=keyboard)
        print("inside fight")

    elif call.data == "attack_b": # делает атаку по enemy1
        player1.defenceoff()
        enemy1.attack()

        #атака по игроку(или оборона)


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

        if enemy1.hp > 0:
            player1.attack()
            bot.send_message(call.message.chat.id, text=random.choice(enemy_attack_pack))
            time.sleep(0.7)
            if player1.attack_flag:
                bot.send_message(call.message.chat.id, text="Скелет попадает по вам!")
            else:
                bot.send_message(call.message.chat.id, text="Но скелет не попадает по вам!")
            time.sleep(0.7)

            print("inside attack")
        elif enemy1.hp <= 0:
            # bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету,\
            #  он разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами \
            #  некогда \"живого\" скелета, который больше не представляет никакой угрозы.")
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Осмотреть труп скелета', callback_data='looting')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету, он разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.", reply_markup=keyboard)

        if player1.hp <= 0:
            bot.send_message(call.message.chat.id, text='Скелет делает решительный выпад. Вы пытаетесь его атаку, но мешкаете, и не успеваете подставить свой кинжал под его удар. Ржавый скелета прорубает ваше левое плечо, после чего застревает там. Вы не чувствуете боли, лишь только то, как ваши силы покидают вас и вам хочется прилечь отдохнуть. Просто отдохнуть...')
            time.sleep(2)
            bot.send_message(call.message.chat.id, text='Вы погибли! Чтобы начать заново, напишите "/start".')
        elif enemy1.hp > 0 and player1.hp > 0:
            bot.send_message(call.message.chat.id,
                             text="Ваш HP: " + str(player1.hp) + " HP\nHP скелета: " + str(enemy1.hp) + " HP",
                             reply_markup=keyboard)


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

        enemy1.hp -= 2
        print(player1.kz)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text=random.choice(players_safe_attack_pack))
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, text="Вы попадаете по скелету и готовы отражать его атаку!")
        time.sleep(0.7)


        if enemy1.hp > 0:
            player1.attack()
            bot.send_message(call.message.chat.id, text=random.choice(enemy_attack_pack))
            time.sleep(0.7)
            if player1.attack_flag:
                bot.send_message(call.message.chat.id, text="Скелет попадает по вам!")
            else:
                bot.send_message(call.message.chat.id, text="Но скелет не попадает по вам!")
            time.sleep(0.7)

        elif enemy1.hp <= 0:
            bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету,он разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.")
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Осмотреть труп скелета', callback_data='looting')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету, он разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.",
                             reply_markup=keyboard)
        if player1.hp <= 0:
            bot.send_message(call.message.chat.id, text='Скелет делает решительный выпад. Вы пытаетесь блокировать его атаку, но мешкаете, и не успеваете подставить свой кинжал под его удар. Ржавый меч скелета прорубает ваше левое плечо, после чего застревает там. Вы не чувствуете боли, лишь только то, как ваши силы покидают вас и вам хочется прилечь отдохнуть. Просто отдохнуть...')
            time.sleep(2)
            bot.send_message(call.message.chat.id, text='Вы погибли! Чтобы начать заново, напишите "/start".')
        elif enemy1.hp > 0 and player1.hp > 0:
            bot.send_message(call.message.chat.id,
                             text="Ваш HP: " + str(player1.hp) + " HP\nHP скелета: " + str(enemy1.hp) + " HP",
                             reply_markup=keyboard)


    elif call.data == "hill":
        if player1.hillC > 0 and player1.hp < 20:
            plhp = player1.hp
            player1.hill()
            player1.defenceoff()
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')',callback_data='hill')
            keyboard.add(key_oven)
            player1.hill()
            plhp = player1.hp - plhp
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
            time.sleep(0.7)
            bot.send_message(call.message.chat.id, text=random.choice(players_hill_pack))
            time.sleep(0.7)
            bot.send_message(call.message.chat.id, text=f"Вы восстановили {plhp} HP!")
            time.sleep(0.7)


            if enemy1.hp > 0:
                player1.attack()
                bot.send_message(call.message.chat.id, text=random.choice(enemy_attack_pack))
                time.sleep(0.7)
                if player1.attack_flag:
                    bot.send_message(call.message.chat.id, text="Скелет попадает по вам!")
                else:
                    bot.send_message(call.message.chat.id, text="Но скелет не попадает по вам!")
                time.sleep(0.7)

            elif enemy1.hp <= 0:
                bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету, разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.")
                keyboard = types.InlineKeyboardMarkup()
                key_oven = types.InlineKeyboardButton(text='Осмотреть труп скелета', callback_data='looting')
                keyboard.add(key_oven)
                bot.send_message(call.messege.chat.id, text="С последним решительным ударом, который вы нанесли скелету, он разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.",
                                 reply_markup=keyboard)
            if player1.hp <= 0:
                bot.send_message(call.message.chat.id, text='Скелет делает решительный выпад. Вы пытаетесь блокировать его атаку, но мешкаете, и не успеваете подставить свой кинжал под его удар. Ржавый меч скелета прорубает ваше левое плечо, после чего застревает там. Вы не чувствуете боли, лишь только то, как ваши силы покидают вас и вам хочется прилечь отдохнуть. Просто отдохнуть...')
                time.sleep(2)
                bot.send_message(call.message.chat.id, text='Вы погибли! Чтобы начать заново, напишите "/start".')
            elif enemy1.hp > 0 and player1.hp > 0:
                bot.send_message(call.message.chat.id,
                                 text="Ваш HP: " + str(player1.hp) + " HP\nHP скелета: " + str(enemy1.hp) + " HP",
                                 reply_markup=keyboard)
        elif player1.hp == 20:
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

    elif call.data == 'looting': # Вот сюда нужно меня выкинуть после победы.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        flags['skeleton_fight'] = 1
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Пройти дальше к двери', callback_data='gnome_door')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Вернуться к выходу из первой комнаты', callback_data='crossroads')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы решаете осмотреть развалины скелета, чтобы проверить, есть ли на нем что-либо интересное.'\
                        ' Ржавый меч, который он держал, кажется абсолютно бесполезным и сломанным, но ваш взгляд упирается в маленький флакончик с голубой жидкостью, который был прикреплен к его поясу.'\
                        ' Вы осторожно берете флакончик и осматриваете его. Голубая жидкость кажется сверкающей и магической. Вы осознаете, что это зелье, которое, возможно, может быть полезным в будущем.', reply_markup=keyboard)



bot.polling(none_stop=True, interval=0)