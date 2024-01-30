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

#  Files
import config
import inline_markups
import reply_markups





#  Aiogram Variables
storage = MemoryStorage()
bot = Bot(config.telegram_api_token)
dp = Dispatcher(bot, storage = MemoryStorage())

#  Sqlite3 Variables
db = sqlite3.connect('database.db', check_same_thread = False)
sql = db.cursor()

#  Datetime Variables
date_time = datetime.datetime.now().date()





#  Add New User data
async def add_new_user(message):
    sql.execute('INSERT INTO user_access (id, username, firstname, lastname, date) VALUES (?, ?, ?, ?, ?)',
    (message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, date_time))
    sql.execute('INSERT INTO user_favorite (id, business, cooking, education, fashion, gaming, music, technology, science) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (message.chat.id, 0, 0, 0, 0, 0, 0, 0, 0))
    sql.execute('INSERT INTO user_action (id, action) VALUES (?, ?)',
    (message.chat.id, '-'))
    db.commit()





















#  Delete Text Message (1)
async def delete_text_message_1(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    except:
        pass

#  Delete Text Message (2)
async def delete_text_message_2(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass

#  Delete Text Message (3)
async def delete_text_message_3(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 2)
    except:
        pass




#  Delete Call Message (1)
async def delete_call_message_1(call):
    try:
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    except:
        pass

#  Delete Call Message (2)
async def delete_call_message_2(call):
    try:
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id - 1)
    except:
        pass

#  Delete Call Message (3)
async def delete_call_message_3(call):
    try:
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id - 1)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id - 2)
    except:
        pass