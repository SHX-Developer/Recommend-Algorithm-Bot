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





#  Aiogram Variables
storage = MemoryStorage()
bot = Bot(config.telegram_api_token)
dp = Dispatcher(bot, storage = MemoryStorage())

#  Sqlite3 Variables
db = sqlite3.connect('database.db', check_same_thread = False)
sql = db.cursor()

#  Datetime Variables
date_time = datetime.datetime.now().date()





#  Favorite
async def display_favorite(message):
    business = sql.execute(f'SELECT business FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    cooking = sql.execute(f'SELECT cooking FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    education = sql.execute(f'SELECT education FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    fashion = sql.execute(f'SELECT fashion FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    gaming = sql.execute(f'SELECT gaming FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    music = sql.execute(f'SELECT music FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    technology = sql.execute(f'SELECT technology FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    science = sql.execute(f'SELECT science FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]

    await bot.send_message(
        chat_id = message.chat.id, 
        text = 
        '<i><b>❤️  Your likes:</b></i>'
        f'\n\nBusiness:   <b>{business}</b>'
        f'\nCooking:   <b>{cooking}</b>'
        f'\nEducation:   <b>{education}</b>'
        f'\nFashion:   <b>{fashion}</b>'
        f'\nGaming:   <b>{gaming}</b>'
        f'\nMusic:   <b>{music}</b>'
        f'\nTechnology:   <b>{technology}</b>'
        f'\nScience:   <b>{science}</b>',
        parse_mode = 'html')







#  Recomend (Message)
async def display_recomend_message(message):

    # Получение суммы лайков для каждой категории
    business = sql.execute(f'SELECT business FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    cooking = sql.execute(f'SELECT cooking FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    education = sql.execute(f'SELECT education FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    fashion = sql.execute(f'SELECT fashion FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    gaming = sql.execute(f'SELECT gaming FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    music = sql.execute(f'SELECT music FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    technology = sql.execute(f'SELECT technology FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    science = sql.execute(f'SELECT science FROM user_favorite WHERE id = {message.chat.id}').fetchone()[0]
    
    # Определение категории с наибольшей суммой лайков
    favorite_category = max(business, cooking, education, fashion, gaming, music, technology, science)

    if favorite_category == business:
        favorite_category_name = 'business'
    elif favorite_category == cooking:
        favorite_category_name = 'cooking'
    elif favorite_category == education:
        favorite_category_name = 'education'
    elif favorite_category == fashion:
        favorite_category_name = 'fashion'
    elif favorite_category == gaming:
        favorite_category_name = 'gaming'
    elif favorite_category == music:
        favorite_category_name = 'music'
    elif favorite_category == technology:
        favorite_category_name = 'technology'
    elif favorite_category == science:
        favorite_category_name = 'science'
    
    # Генерация случайного числа для добавления некоторой степени случайности
    random_value = random.random()
    value = round(random_value, 5)

    # Вероятность рекомендации категории с наибольшей суммой лайков
    probability_threshold = 0.6

    if random_value < probability_threshold:
        recommended_category = favorite_category_name
        
    else:
        # Если random_value >= probability_threshold, отправляем случайную категорию, кроме той, которая им нравится больше
        available_categories = ['business', 'cooking', 'education', 'fashion', 'gaming', 'music', 'technology', 'science']
        available_categories.remove(favorite_category_name)
        recommended_category = random.choice(available_categories)
        
    # Обновление базы данных и отправка рекомендации
    sql.execute('UPDATE user_action SET action = ? WHERE id = ?', (recommended_category, message.chat.id))
    db.commit()
    
    await bot.send_message(
        chat_id = message.chat.id, 
        text = 
        f'✅  Recommended category:   <b>{recommended_category}</b>'
        '\n\n\n<b><i>❤️  Your likes:</i></b>'
        f'\nBusiness:   <b>{business}</b>'
        f'\nCooking:   <b>{cooking}</b>'
        f'\nEducation:   <b>{education}</b>'
        f'\nFashion:   <b>{fashion}</b>'
        f'\nGaming:   <b>{gaming}</b>'
        f'\nMusic:   <b>{music}</b>'
        f'\nTechnology:   <b>{technology}</b>'
        f'\nScience:   <b>{science}</b>'
        '\n\n\n<b><i>⚙️  Recomendation algorithm:</i></b>'
        '\n😍  0.1  -  0.7:   <b>Favorite category</b>'
        '\n🤨  0.7  -  1.0:   <b>Random category</b>'
        f'\n\n\n🪄  Probability:   <b>{value}</b>',
        parse_mode = 'html', 
        reply_markup = inline_markups.action_inline)







#  Recomend (Call)
async def display_recomend_call(call):
    
    # Получение суммы лайков для каждой категории
    business = sql.execute(f'SELECT business FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    cooking = sql.execute(f'SELECT cooking FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    education = sql.execute(f'SELECT education FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    fashion = sql.execute(f'SELECT fashion FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    gaming = sql.execute(f'SELECT gaming FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    music = sql.execute(f'SELECT music FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    technology = sql.execute(f'SELECT technology FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    science = sql.execute(f'SELECT science FROM user_favorite WHERE id = {call.message.chat.id}').fetchone()[0]
    
    # Определение категории с наибольшей суммой лайков
    favorite_category = max(business, cooking, education, fashion, gaming, music, technology, science)

    if favorite_category == business:
        favorite_category_name = 'business'
    elif favorite_category == cooking:
        favorite_category_name = 'cooking'
    elif favorite_category == education:
        favorite_category_name = 'education'
    elif favorite_category == fashion:
        favorite_category_name = 'fashion'
    elif favorite_category == gaming:
        favorite_category_name = 'gaming'
    elif favorite_category == music:
        favorite_category_name = 'music'
    elif favorite_category == technology:
        favorite_category_name = 'technology'
    elif favorite_category == science:
        favorite_category_name = 'science'
    
    # Генерация случайного числа для добавления некоторой степени случайности
    random_value = random.random()
    value = round(random_value, 5)

    # Вероятность рекомендации категории с наибольшей суммой лайков
    probability_threshold = 0.6

    if random_value < probability_threshold:
        recommended_category = favorite_category_name
        
    else:
        # Если random_value >= probability_threshold, отправляем случайную категорию, кроме той, которая им нравится больше
        available_categories = ['business', 'cooking', 'education', 'fashion', 'gaming', 'music', 'technology', 'science']
        available_categories.remove(favorite_category_name)
        recommended_category = random.choice(available_categories)
        
    # Обновление базы данных и отправка рекомендации
    sql.execute('UPDATE user_action SET action = ? WHERE id = ?', (recommended_category, call.message.chat.id))
    db.commit()
    
    await bot.send_message(
        chat_id = call.message.chat.id, 
        text = 
        f'✅  Recommended category:   <b>{recommended_category}</b>'
        '\n\n\n<b><i>❤️  Your likes:</i></b>'
        f'\nBusiness:   <b>{business}</b>'
        f'\nCooking:   <b>{cooking}</b>'
        f'\nEducation:   <b>{education}</b>'
        f'\nFashion:   <b>{fashion}</b>'
        f'\nGaming:   <b>{gaming}</b>'
        f'\nMusic:   <b>{music}</b>'
        f'\nTechnology:   <b>{technology}</b>'
        f'\nScience:   <b>{science}</b>'
        '\n\n\n<b><i>⚙️  Recomendation algorithm:</i></b>'
        '\n😍  0.1  -  0.7:   <b>Favorite category</b>'
        '\n🤨  0.7  -  1.0:   <b>Random category</b>'
        f'\n\n\n🪄  Probability:   <b>{value}</b>',
        parse_mode = 'html', 
        reply_markup = inline_markups.action_inline)