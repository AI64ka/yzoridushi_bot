import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    MenuButtonWebApp,
)
from aiogram.filters import CommandStart

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

WEBAPP_URL = "https://ai64ka.github.io/yzoridushi_bot/"


SECTIONS = {
    "paintings": "🖼 Картины — открой витрину кнопкой выше, чтобы посмотреть работы.",
    "courses": "🎨 Обучение диджитал-рисованию — подробности в витрине.",
    "arttherapy": "🧘 Арт-терапия — запись в витрине.",
    "consult": "💬 Личная консультация — запись в витрине.",
    "merch": "🛍 Мерч — товары в витрине.",
}


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎨 Открыть витрину", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="🖼 Картины", callback_data="paintings")],
        [InlineKeyboardButton(text="🎨 Обучение рисованию", callback_data="courses")],
        [InlineKeyboardButton(text="🧘 Арт-терапия", callback_data="arttherapy")],
        [InlineKeyboardButton(text="💬 Личная консультация", callback_data="consult")],
        [InlineKeyboardButton(text="🛍 Мерч", callback_data="merch")],
    ])


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Это бот Daniel Ramo 🎨\n\nНажми «Открыть витрину», чтобы посмотреть работы и записаться:",
        reply_markup=main_menu(),
    )


@dp.callback_query(F.data.in_(SECTIONS))
async def section_handler(callback: CallbackQuery):
    await callback.message.answer(SECTIONS[callback.data])
    await callback.answer()


async def main():
    # постоянная кнопка "Витрина" рядом с полем ввода
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Витрина", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())