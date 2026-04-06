import asyncio
import sqlite3
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiohttp import web  # Обязательно для Render

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8729349351:AAGq0KrBofZVpnG1pJuyPbvEndY9jk6jCPQ"
ADMIN_ID = 5737961034 
MY_USERNAME = "@yng_beko"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='Markdown'))
dp = Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (ЧТОБЫ НЕ ЗАСЫПАЛ) ---
async def handle(request):
    return web.Response(text="Jerk Store is Live!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

# --- БАЗА ДАННЫХ ---
def init_db():
    conn = sqlite3.connect('jerk_store.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, username TEXT, expiry_date TEXT, status TEXT DEFAULT 'inactive')''')
    conn.commit()
    conn.close()

# --- ГЛАВНОЕ МЕНЮ (ОБНОВЛЕННЫЕ НАЗВАНИЯ) ---
def main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📦 ЗАКАЗАТЬ РОУТЕР", callback_data="buy"))
    builder.row(types.InlineKeyboardButton(text="🌐 МОЯ ПОДПИСКА", callback_data="my_sub"))
    builder.row(types.InlineKeyboardButton(text="🛠 ПОДДЕРЖКА", callback_data="support"))
    return builder.as_markup()

# --- ОБРАБОТЧИКИ (ТЕПЕРЬ ПИШУТ НОВЫЕ СООБЩЕНИЯ) ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    conn = sqlite3.connect('jerk_store.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', 
                   (message.from_user.id, message.from_user.username))
    conn.commit()
    conn.close()
    
    await message.answer(
        f"👋 Йо, **{message.from_user.first_name}**!\n\n"
        "Добро пожаловать в **JERK STORE** 🔌\n\n"
        "Выбирай нужный раздел ниже: 👇", 
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "buy