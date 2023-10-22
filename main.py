import random
import telebot
from  telebot import types
import time


bot = telebot.TeleBot('6682494061:AAFLZH7Qj32HYffI2UQdgpXxj0giooBe5iQ')


flags = {'first_room_searched':0,'torch_acq':0,'first_key_acq':0,'stupid':0}

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        global flags
        flags = {'first_room_searched':0,'torch_acq':0,'first_key_acq':0,'stupid':0}
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
    
    elif call.data == 'crossroads':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=None)
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Пойти налево',callback_data='fight_loop')
        keyboard.add(key_oven)
        key_oven = types.InlineKeyboardButton(text='Пойти направо',callback_data='fountain_door')
        keyboard.add(key_oven)
        bot.send_message(call.message.chat.id,text='Достав ключ из своих карманов, вы вставили его в замочную скважину. Повернув ключ, вы услышали щелчок, и замок отперся. Откинув замок в сторону, вы аккуратно проходите через дверь.'\
                        ' Вы оказываетесь в узком, холодном каменном коридоре, который тянется в обе стороны. Ваши воспоминания о прошлом остаются пустыми, и перед вами стоит выбор, который наполняет вас некоторым беспокойством. Слева от вас слышатся странные, приглушенные звуки, будто что-то движется по каменному полу.'\
                        ' Справа от вас раздаются звуки, напоминающие плеск воды.',reply_markup=keyboard)



bot.polling(none_stop=True, interval=0)