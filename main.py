import asyncio
import sqlite3
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8729349351:AAGq0KrBofZVpnG1pJuyPbvEndY9jk6jCPQ"
ADMIN_ID = 5737961034 
MY_USERNAME = "@yng_beko"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='Markdown'))
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect('jerk_store.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, username TEXT, expiry_date TEXT, status TEXT DEFAULT 'inactive')''')
    conn.commit()
    conn.close()

def main_menu():
    builder = InlineKeyboardBuilder()
    # Обновил названия кнопок по твоему запросу
    builder.row(types.InlineKeyboardButton(text="📦 ЗАКАЗАТЬ РОУТЕР (С VPN)", callback_data="buy"))
    builder.row(types.InlineKeyboardButton(text="🌐 МОЯ ПОДПИСКА", callback_data="my_sub"))
    builder.row(types.InlineKeyboardButton(text="🛠 ПОДДЕРЖКА", callback_data="support"))
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    conn = sqlite3.connect('jerk_store.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', 
                   (message.from_user.id, message.from_user.username))
    conn.commit()
    conn.close()
    await message.answer(
        f"👋 Пивет, **{message.from_user.first_name}**!\n\n"
        "Добро пожаловать в **JERK STORE** 🔌\n\n"
        "Выбирай пункт в меню ниже: 👇", 
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "buy")
async def buy_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔥 **ПРАЙС-ЛИСТ JERK STORE** 🔥\n\n"
        "📦 **Standard Pack** — `9 800 ₽` \n\n"
        "🏆 **Ultra Cyber Pack** — `19 800 ₽` \n\n"
        f"💳 По вопросам пиши: {MY_USERNAME}\n"
        f"🆔 Твой ID: `{callback.from_user.id}`",
        reply_markup=main_menu()
    )
    await bot.send_message(ADMIN_ID, f"🔔 **ИНТЕРЕС К ПОКУПКЕ!**\nЮзер: @{callback.from_user.username}")
    await callback.answer()

@dp.callback_query(F.data == "my_sub")
async def check_sub(callback: types.CallbackQuery):
    conn = sqlite3.connect('jerk_store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT expiry_date, status FROM users WHERE user_id = ?', (callback.from_user.id,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0]:
        icon = "✅" if row[1] == "active" else "❌"
        await callback.message.edit_text(f"📊 **СТАТУС:** {icon} {row[1]}\nДо: `{row[0]}`", reply_markup=main_menu())
    else:
        await callback.message.edit_text("😢 Нет активных услуг.", reply_markup=main_menu())
    await callback.answer()

@dp.callback_query(F.data == "support")
async def support_info(callback: types.CallbackQuery):
    await callback.message.edit_text(f"👨‍💻 **ТЕХПОДДЕРЖКА**\n\nПиши: {MY_USERNAME}", reply_markup=main_menu())
    await callback.answer()

@dp.message(Command("activate"))
async def activate_user(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        _, uid, days = message.text.split()
        expiry = (datetime.now() + timedelta(days=int(days))).strftime("%Y-%m-%d")
        conn = sqlite3.connect('jerk_store.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET expiry_date = ?, status = "active" WHERE user_id = ?', (expiry, int(uid)))
        conn.commit()
        conn.close()
        await message.answer(f"✅ Готово! ID {uid} активен до {expiry}")
    except:
        await message.answer("Ошибка! Юзай: `/activate ID ДНИ`")

async def main():
    init_db()
    print("🚀 JERK STORE IS ONLINE!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())