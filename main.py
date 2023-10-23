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
flags = {'first_room_searched':0,'torch_acq':0,'first_key_acq':0,'stupid':0,'crossroads':0,'skeleton_fight':0,'gnome_killed':0,'gnome_relationship':2,'gerard':0,'who':0,'golden_key':0,'fountain_room_checked':0,'door_opened':0}

bot = telebot.TeleBot('6682494061:AAFLZH7Qj32HYffI2UQdgpXxj0giooBe5iQ')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        global flags
        global player1

        player1 = Player(hp=20, kz=14, kz_flag=0, hillC=1, attack_flag=0) # изменять для тестирования праметры игрока
        flags = {'first_room_searched':0,'torch_acq':0,'first_key_acq':0,'stupid':0,'crossroads':0,'skeleton_fight':0,'gnome_killed':0,'gnome_relationship':2,'gerard':0,'who':0,'golden_key':0,'fountain_room_checked':0,'door_opened':0}
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
                        ' Воздух в этом месте неприятно холодный, и вам непонятно, как вы оказались здесь. Ваши воспоминания исчезли,'\
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
        if flags['crossroads'] == 0:
            bot.send_message(call.message.chat.id,text='Достав ключ из своих карманов, вы вставили его в замочную скважину. Повернув ключ, вы услышали щелчок, и замок отперся. Откинув замок в сторону, вы аккуратно проходите через дверь.'\
                            ' Вы оказываетесь в узком, холодном каменном коридоре, который тянется в обе стороны. Ваши воспоминания о прошлом остаются пустыми, и перед вами стоит выбор, который наполняет вас некоторым беспокойством. Слева от вас слышатся странные, приглушенные звуки, будто что-то движется по каменному полу.'\
                            ' Справа от вас раздаются звуки, напоминающие плеск воды.',reply_markup=keyboard)
            flags['crossroads'] = 1
        else:
            bot.send_message(call.message.chat.id,text='Вы вернулись ко входу в комнату вашего заточения. Куда пойдете?',reply_markup=keyboard)

    ### НИЖЕ КОД БОЯ

    elif call.data == "fight_loop": # запускает круг боя(условия выхода пока нет)
        global enemy1
        enemy1 = Npc(hp=3, kz=10, kz_flag=0, attack_flag=0) # изменять для тестирования праметры противника
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
            #bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету,он разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.")
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
                #bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету, разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.")
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

    #
    #бой со вторым противником ниже
    #
    elif call.data == "fight_loop_final": # запускает круг боя(условия выхода пока нет)
        enemy1 = Npc(hp=3, kz=10, kz_flag=0, attack_flag=0) # изменять для тестирования праметры противника
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=None)
        bot.send_message(call.message.chat.id,text='Повернув влево и приближаясь к источнику странных звуков, ваше сердце начинает биться сильнее от страха и неизвестности. По мере продвижения по коридору, вы видите что-то, что быстро вызывает в вас тревожное волнение.'\
                        ' Ваш взгляд падает на живого скелета, бездумно бродящего вдоль коридора. В его руках вы видите ржавый меч. Скелет явно заметил ваше присутствие и направил свой меч в вашем направлении.',reply_markup=None)
        time.sleep(1)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b_final')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b_final')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось '+str(player1.hillC)+')', callback_data='hill_final')
        keyboard.add(key_oven)
        time.sleep(0.7)
        bot.send_message(call.message.chat.id, "Выберите действие!", reply_markup=keyboard)
        print("inside fight")

    elif call.data == "attack_b_final": # делает атаку по enemy1
        player1.defenceoff()
        enemy1.attack()

        #атака по игроку(или оборона)


        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b_final')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b_final')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')',callback_data='hill_final')
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


    elif call.data == "defence_b_final":
        player1.defenceoff()
        print("inside defence")
        player1.defence()
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b_final')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b_final')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')', callback_data='hill_final')
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
            #bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету,он разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.")
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


    elif call.data == "hill_final":
        if player1.hillC > 0 and player1.hp < 20:
            plhp = player1.hp
            player1.hill()
            player1.defenceoff()
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b_final')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b_final')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')',callback_data='hill_final')
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
                #bot.send_message(call.message.chat.id, text="С последним решительным ударом, который вы нанесли скелету, разлетается на кучу костей с характерным звуком. Теперь вы стоите перед развалинами некогда \"живого\" скелета, который больше не представляет никакой угрозы.")
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
            key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b_final')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b_final')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')',callback_data='hill_final')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id, text="Вы и так полностью здоровы.", reply_markup=keyboard)
        else:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            time.sleep(0.7)
            keyboard = types.InlineKeyboardMarkup()
            key_oven = types.InlineKeyboardButton(text='Атака', callback_data='attack_b_final')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Лёгкая атака с уклонением', callback_data='defence_b_final')
            keyboard.add(key_oven)
            key_oven = types.InlineKeyboardButton(text='Выпить зелье лечения (осталось ' + str(player1.hillC) + ')', callback_data='hill_final')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id, text="У вас кончились зелья лечения!", reply_markup=keyboard)



    #
    # бой со вторым противником выше
    #



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
        
    elif call.data == 'dead_skeleton': # "Комната" с мертвым скетелом после первой интеракции с ним.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Пройти дальше к двери', callback_data='gnome_door')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Вернуться к выходу из первой комнаты', callback_data='crossroads')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы подходите к трупу поверженного вами скелета. Его череп, лежащий на холодных каменных плитах, смотрит на вас отсутствующими глазами.',reply_markup=keyboard)

    elif call.data == 'gnome_door': # Дверь у комнаты гнома.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        if flags['gerard'] == 0 and flags['gnome_killed'] == 0:
            key_oven = types.InlineKeyboardButton(text='Открыть дверь и зайти', callback_data='gnome_room')
            keyboard.add(key_oven)
        if flags['gerard'] == 1 and flags['who'] == 1:
            key_oven = types.InlineKeyboardButton(text='Открыть дверь и зайти', callback_data='gnome_room_alive')
            keyboard.add(key_oven)
        if flags['gnome_killed'] == 1:
            key_oven = types.InlineKeyboardButton(text='Открыть дверь и зайти', callback_data='gnome_room_dead')
            keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Отойти к трупу скелета',callback_data='dead_skeleton')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы оказываетесь у деревянной двери без какого-либо видимого замка. Вокруг двери, на стенах, нет ничего примечательного. Что делаете?',reply_markup=keyboard)

    elif call.data == 'gnome_room': # Вход в комнату гнома, первая.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Подойти к гному и дереву',callback_data='near_gnome_alive')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выйти из комнаты',callback_data='gnome_door')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Зайдя в комнату, вы наблюдаете странную картину - внутри каменной, освещенной непонятным способом комнаты стоит дерево (судя по яблокам, висящих на ветках, яблоня), под которым сидит синебородый старый гном в шляпе.',reply_markup=keyboard)

    elif call.data == 'gnome_room_dead': # Вход в комнату гнома, когда он убит.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Выйти из комнаты',callback_data='gnome_door')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы отошли от трупа гнома. Вам больше не о чем с ним говорить.',reply_markup=keyboard)

    elif call.data == 'gnome_room_alive': # Вход в комнату гнома, когда он живой.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Подойти к гному и дереву',callback_data='near_gnome_alive')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выйти из комнаты',callback_data='gnome_door')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы стоите около двери, поодаль от гнома и дерева.',reply_markup=keyboard)

    elif call.data == 'near_gnome_alive': # Начать ветку диалога с гномом.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        if (flags['who'] == 0 and flags['gerard'] == 0) or (flags['who'] == 0 and flags['gerard'] == 1) or (flags['who'] == 1 and flags['gerard'] == 0):
            key_oven = types.InlineKeyboardButton(text='Пырнуть гнома',callback_data='gnome_killer')
            keyboard.add(key_oven)
        if flags['gerard'] == 0:
            key_oven = types.InlineKeyboardButton(text='"Меня зовут Жерард..?"',callback_data='dialogue_gerard')
            keyboard.add(key_oven)
        if flags['who'] == 0:
            key_oven = types.InlineKeyboardButton(text='"А кто ты?"',callback_data='dialogue_who')
            keyboard.add(key_oven)
        if flags['who'] == 1 and flags['gerard'] == 1:
            key_oven = types.InlineKeyboardButton(text='"Что мне делать теперь?"',callback_data='dialogue_what_to_do')
            keyboard.add(key_oven)
        if flags['who'] == 0 and flags['gerard'] == 0:
            bot.send_message(call.message.chat.id, text='Вы подходите к сидящему гному. Он обращается к вам:\n - Здравствуй, Жерард. Ты нашел ключ, который я спрятал!',reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, text='Гном смотрит на вас.',reply_markup=keyboard)

    elif call.data == 'gnome_killer': # Вы убили старого гнома. У вас нет души.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Подобрать яблоко с земли и съесть',callback_data='yum')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Обыскать труп',callback_data='gnome_looting')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Душа? Нет, у меня такой нет.',callback_data='no_soul')
        keyboard.add(key_oven)
        flags['gnome_killed'] = 1
        bot.send_message(call.message.chat.id, text='Вы решили, что этот гном со своей крашеной синей бородой вас слишком сильно раздражает, выхватили кинжал и пырнули его в живот.\
                         \n- Жерард... За что?\nВы безэмоционально вытаскиваете кинжал из его живота и смотрите, как он истекает кровью. У вас вообще есть душа?',reply_markup=keyboard)

    elif call.data == 'no_soul': # Я такая мета-мета!
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, text='Да? Наверное, вы этого не осознаете, но если у вас нет души, то вы не живете.\nСледовательно, вы погибли! Если хотите начать заново, то напишите "/start". И подыщите себе душу.')

    elif call.data == 'yum': # Съел яблоко.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Вернуться к трупу гнома',callback_data='gnome_looting')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы подобрали яблоко, лежащее рядом с трупом бессердечно убитого гнома и съели. На него попало немного крови вашей жертвы, но вас это не смутило. Питательно!', reply_markup=keyboard)

    elif call.data == 'gnome_looting': # Обыск гнома.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Отойти от трупа',callback_data='gnome_room_dead')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы осматриваете труп гнома. В его кармане вы обнаруживаете золотой ключ. Интересно, от какого он замка?', reply_markup=keyboard)

    elif call.data == 'dialogue_gerard': # Ветка диалога "меня зовут Жерард?"
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='"Мой отец запер меня здесь?"',callback_data='dialogue_father')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='"Какое ужасное у меня имя."',callback_data='dialogue_horrible_name')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='- Именно так! А если быть точным, тебя зовут Жерард Опэн фон Эйайович III.'\
                        ' Твой отец, Жерард Опэн фон Эйайович II, запер тебя здесь.',reply_markup=keyboard)
    
    elif call.data == 'dialogue_horrible_name': # Плохое имя.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        flags['gnome_relationship'] -= 1
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='"Оу. А что там про отца?"',callback_data='dialogue_father')
        keyboard.add(key_oven)
        flags['gerard'] = 1
        bot.send_message(call.message.chat.id, text='- Вообще-то это имя было придумано мной.',reply_markup=keyboard)
    
    elif call.data == 'dialogue_father': # Отец.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='"Отец года..."',callback_data='near_gnome_alive')
        keyboard.add(key_oven)
        flags['gerard'] = 1
        bot.send_message(call.message.chat.id, text='- Жерард II запер тебя здесь из-за того, что боялся. Он настолько боялся твоего внутреннего магического таланта, что отправил тебя в заточение, стерев тебе все воспоминания.',reply_markup=keyboard)

    elif call.data == 'dialogue_who': # Кто гном такой?
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        flags['who'] = 1
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='"И при этом ты просто сидишь здесь."',callback_data='dialogue_useless')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='"Мне повезло иметь такого союзника!"',callback_data='dialogue_flattery')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='- Я - легендарный маг, твой учитель магии, тот, кто воспитывал тебя с самого детства!',reply_markup=keyboard)

    elif call.data == 'dialogue_useless': # Обиделся.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        flags['gnome_relationship'] -= 1
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='"Ну, чтож, раз так..."',callback_data='near_gnome_alive')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='- Я уже сделал, все что мог, мальчишка! Твой отец невероятно силен.',reply_markup=keyboard)

    elif call.data == 'dialogue_flattery': # Порадовался.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='"Хм."',callback_data='near_gnome_alive')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='- Именно, именно!\nГном ухмыльнулся.',reply_markup=keyboard)

    elif call.data == 'dialogue_what_to_do': # Выход из диалога.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='"Не прощаемся..."',callback_data='gnome_room_alive')
        keyboard.add(key_oven)
        flags['golden_key'] = 1
        bot.send_message(call.message.chat.id, text='- Хм... Возможно, ты сможешь уговорить своего отца - ведь ты не помнишь ни одного магического слова... Так и быть, стоит рискнуть. Держи, это ключ от комнаты Жерарда. Она дальше по коридору. Не прощаемся!',reply_markup=keyboard)


    elif call.data == 'fountain_door': # Проход направо с распутья.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Зайти в дверь',callback_data='fountain_room')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы проходите направо. Лишь только факел позволяет вам что-то видеть в местной кромешной темноте. Звук воды усиливается, и через пару минут вы доходите до деревянной двери.',reply_markup=keyboard)

    elif call.data == 'fountain_room': # Комната с фонтаном и маленькой дыркой.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        if flags['fountain_room_checked'] == 0:
            key_oven = types.InlineKeyboardButton(text='Осмотреть комнату повнимательнее',callback_data='i_love_hse')
            keyboard.add(key_oven)
        if flags['fountain_room_checked'] == 1 and flags['door_opened'] == 0:
            key_oven = types.InlineKeyboardButton(text='Подойти к дырке',callback_data='i_love_hse')
            keyboard.add(key_oven)
        if flags['door_opened'] == 1:
            key_oven = types.InlineKeyboardButton(text='Подойти к иллюзионной двери',callback_data='i_love_hse')
            keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Подойти к фонтану',callback_data='fountain')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Выйти из комнаты до распутья',callback_data='crossroads')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Перед вами небольшая комната, и источник тех самых звуков - фонтан с водой.',reply_markup=keyboard)

    elif call.data == 'i_love_hse': # Обыскивание комнаты, после станет подходом к дырке.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        if flags['skeleton_fight'] == 1 and flags['door_opened'] == 0:
            key_oven = types.InlineKeyboardButton(text='Попробовать выпить подобранное зелье',callback_data='after_fountain')
            keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Пойти в центр комнаты',callback_data='fountain_room')
        keyboard.add(key_oven)
        if flags['fountain_room_checked'] == 0:
            bot.send_message(call.message.chat.id, text='Походив и поизучав комнату, вы находите очень маленькую дырку в стене, будто проетую мышью. Очевидно, так просто вам туда не влезть.',reply_markup=keyboard)
        if flags['fountain_room_checked'] == 1 and flags['door_opened'] == 0:
            bot.send_message(call.message.chat.id, text='Вы подошли к дырке в стене.',reply_markup=keyboard)
        flags['fountain_room_checked'] = 1
        if flags['door_opened'] == 1:
            key_oven = types.InlineKeyboardButton(text='Пойти в скрытую комнату',callback_data='opened_after_fountain')
            keyboard.add(key_oven)
            bot.send_message(call.message.chat.id, text='Вы подошли к неожиданно открытой двери, которая ранее была стеной, со стороны комнаты с фонтаном.',reply_markup=keyboard)

    elif call.data == 'fountain': # Сам фонтан.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Вернуться в центр комнаты',callback_data='fountain_room')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Утопиться',callback_data='drown')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы подошли к фонтану. Это самый непримечательный каменный фонтан, который вы когда-либо видели. Учитывая то, что у вас нет памяти, это не говорит многое об эстетических качествах оного фонтана, но тем не менее - вам не нравится. Но, зато, в нем есть вода. Интересно, она откуда-то поступает или постоянно циркулирует?',reply_markup=keyboard)

    elif call.data == 'drown': # Смерть от утопления.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, text='Вы долго смотрели на свое отражение в воде фонтана и осознали - вы больше не хотите жить. Отбросив факел в сторону, вы легли в воду лицом вниз. Переборов инстинкт самосохранения, судя по всему, потерянный вместе с памятью, вы смогли продержаться до момента потери сознания.\nПосле чего, вы погибли! Для того, чтобы начать заново, напишите "/start".')

    elif call.data == 'after_fountain': # Уменьшение и открытие двери.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Открыть появившуюся дверь',callback_data='i_love_hse')
        flags['door_opened'] = 1
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы выпили зелье и уменьшились до размера, как раз подходящего под эту дыру в стене. Вы спокойно прошли через неё и почти сразу вернули себе свой привычный размер.\nПрежде, чем вы что-либо осмотрели в комнате, в которую зашли, вы заметили, что позади вас есть дверь, которой явно не было с обратной стороны.',reply_markup=keyboard)

    elif call.data == 'opened_after_fountain': # Комната с золотистой дверью.
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Подойти к золотистой двери',callback_data='golden_door')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Вернуться в комнату с фонтаном',callback_data='i_love_hse')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы видите пустую каменную комнату с золотистой дверью спереди и иллюзионной сзади. Очевидно, что эта комната предназначена лишь для создания пустой зоны между иллюзионной дверью позади вас и золотистой спереди.',reply_markup=keyboard)

    elif call.data == 'golden_door':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Отойти от двери',callback_data='opened_after_fountain')
        keyboard.add(key_oven)
        if flags['gnome_killed'] == 1 or flags['golden_key'] == 1:
            key_oven = types.InlineKeyboardButton(text='Попробовать открыть дверь золотым ключом',callback_data='fight_loop_final')
            keyboard.add(key_oven)
        bot.send_message(call.message.chat.id, text='Вы подходите к золотистой двери, замок которой встроен непосредственно в саму дверь.',reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)