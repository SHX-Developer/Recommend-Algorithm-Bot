#  Aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

#  Libraries
import sqlite3
import datetime
import asyncio
import random

#  Files
import config
import inline_markups
import reply_markups
import functions
import display

from data import (
greeting_text, menu_text, help_text)




#  Aiogram Variables
storage = MemoryStorage()
bot = Bot(config.telegram_api_token)
dp = Dispatcher(bot, storage = MemoryStorage())

#  Sqlite3 Variables
db = sqlite3.connect('database.db', check_same_thread = False)
sql = db.cursor()

#  Datetime Variables
date_time = datetime.datetime.now().date()



#  Class States
class States(StatesGroup):
    value = State()



#  Creating Databases
sql.execute('''CREATE TABLE IF NOT EXISTS user_access (
            id INTEGER, 
            username TEXT, 
            firstname TEXT, 
            lastname TEXT, 
            date DATE
            )''')

sql.execute('''CREATE TABLE IF NOT EXISTS user_favorite (
            id INTEGER, 
            business INTEGER,
            cooking INTEGER,
            education INTEGER,
            fashion INTEGER,
            gaming INTEGER,
            music INTEGER,
            technology INTEGER,
            science INTEGER
            )''')

sql.execute('''CREATE TABLE IF NOT EXISTS user_action (
            id INTEGER, 
            action TEXT
            )''')

db.commit()






 
 

 

 
 







#  Command - /start
@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    user_id = sql.execute(f'SELECT id FROM user_access WHERE id = {message.chat.id}').fetchone()

    if user_id == None:
        await functions.add_new_user(message)
        await bot.send_message(message.chat.id, greeting_text, parse_mode = 'html', reply_markup = reply_markups.menu_reply)

    else:
        await bot.send_message(message.chat.id, menu_text, parse_mode = 'html', reply_markup = reply_markups.menu_reply)



#  Command - /help
@dp.message_handler(commands = ['help'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, help_text, parse_mode = 'html', reply_markup = None)






#  Message Handler
@dp.message_handler()
async def text(message: types.Message):
    
    

    if message.text == '🪄  Recommendation':
        await display.display_recomend_message(message)


    elif message.text == '❤️  Favorite':
        await display.display_favorite(message)


    else:
        await bot.send_message(message.chat.id, 'Unknown message !', parse_mode = 'html', reply_markup = None)





#  Callback Handler
@dp.callback_query_handler(lambda call: True)
async def callback_queries(call: types.CallbackQuery):


#  Send Message
    if call.data == 'like':
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        user_action = sql.execute(f'SELECT action FROM user_action WHERE id = {call.message.chat.id}').fetchone()[0]
        sql.execute(f'UPDATE user_favorite SET {user_action} = {user_action} + 1 WHERE id = {call.message.chat.id}')
        db.commit()
        await asyncio.sleep(1)
        await display.display_recomend_call(call)
    
    #  Send Message
    elif call.data == 'dislike':
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        user_action = sql.execute(f'SELECT action FROM user_action WHERE id = {call.message.chat.id}').fetchone()[0]
        sql.execute(f'UPDATE user_favorite SET {user_action} = {user_action} - 1 WHERE id = {call.message.chat.id}')
        db.commit()
        await asyncio.sleep(1)
        await display.display_recomend_call(call)
    
    elif call.data == 'next':
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await asyncio.sleep(1)
        await display.display_recomend_call(call)
        


#  Edit Inline Message
    elif call.data == 'edit_inline':
        await bot.edit_message_text(
            chat_id = call.message.chat.id, 
            message_id = call.message.message_id, 
            text = 'TEXT ', 
            parse_mode = 'html', 
            reply_markup = None)


#  Edit Inline Photo
    if call.data == 'edit_photo':
        with open('photo/photo.jpg', 'rb') as photo:
            bot.edit_message_media( 
                media = types.InputMedia(
                type = 'photo',
                media = photo,
                chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                caption = 'TEXT',
                parse_mode = 'html'),
                reply_markup = None)


#  Delete Inline Message
    elif call.data == 'delete_inline':
        await bot.delete_message(
            chat_id = call.message.chat.id, 
            message_id = call.message.message_id)





#  States
@dp.message_handler(state = States.value)
async def check_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text

        #  Finish State
        if message.text == 'value':
            await state.finish()
        
        #  Set State
        elif message.text == 'value':
            await States.value.set()
        
        #  Next State
        elif message.text == 'value':
            await States.next()
        











#  Message on StartUp
async def start_bot(_):
    await bot.send_message(284929331, 'The bot is successfully enabled ✅')





#  Launch The Bot
if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates = True, on_startup = start_bot)
        except Exception as e:
            print(e)
            continue