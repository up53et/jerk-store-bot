import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# ТОКЕН И ТВОИ ДАННЫЕ
TOKEN = "8729349351:AAGq0KrBofZVpnG1pJuyPbvEndY9jk6jCPQ"
ADMIN_ID = 5737961034 
MY_USERNAME = "@yng_beko"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='Markdown'))
dp = Dispatcher()

# ГЛАВНОЕ МЕНЮ
def main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📦 ЗАКАЗАТЬ РОУТЕР", callback_data="buy"))
    builder.row(types.InlineKeyboardButton(text="🛠 ПОДДЕРЖКА", callback_data="support"))
    return builder.as_markup()

# СТАРТ
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Йо! Это **JERK STORE** 🔌\n\nВыбирай нужный раздел:", 
        reply_markup=main_menu()
    )

# КНОПКА ЗАКАЗАТЬ
@dp.callback_query(F.data == "buy")
async def buy_menu(callback: types.CallbackQuery):
    await callback.message.answer(
        "🔥 **ПРАЙС-ЛИСТ** 🔥\n\n"
        "📦 **Standard** — `9 800 ₽` \n"
        "🏆 **Ultra** — `19 800 ₽` \n\n"
        f"💳 Пиши: {MY_USERNAME}",
        reply_markup=main_menu()
    )
    # Уведомление тебе в личку
    try:
        await bot.send_message(ADMIN_ID, f"🔔 Кто-то нажал кнопку ЗАКАЗАТЬ!")
    except:
        pass
    await callback.answer()

# КНОПКА ПОДДЕРЖКА
@dp.callback_query(F.data == "support")
async def support_info(callback: types.CallbackQuery):
    await callback.message.answer(f"🛠 Пиши сюда: {MY_USERNAME}", reply_markup=main_menu())
    await callback.answer()

async def main():
    print("🚀 БОТ ЗАПУСКАЕТСЯ...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())