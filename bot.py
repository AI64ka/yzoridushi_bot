import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import CommandStart

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


# Разделы: код кнопки -> текст, который покажем при нажатии
SECTIONS = {
    "paintings": "🖼 Картины — здесь будет каталог работ художницы. Скоро!",
    "courses": "🎨 Обучение диджитал-рисованию — описание курса появится здесь.",
    "arttherapy": "🧘 Арт-терапия — запись откроется в мини-аппе.",
    "consult": "💬 Личная консультация — скоро можно будет записаться.",
    "merch": "🛍 Мерч — товары появятся здесь.",
}


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼 Картины", callback_data="paintings")],
        [InlineKeyboardButton(text="🎨 Обучение рисованию", callback_data="courses")],
        [InlineKeyboardButton(text="🧘 Арт-терапия", callback_data="arttherapy")],
        [InlineKeyboardButton(text="💬 Личная консультация", callback_data="consult")],
        [InlineKeyboardButton(text="🛍 Мерч", callback_data="merch")],
    ])


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Это бот Daniel Ramo 🎨\n\nВыбери, что тебя интересует:",
        reply_markup=main_menu(),
    )


@dp.callback_query(F.data.in_(SECTIONS))
async def section_handler(callback: CallbackQuery):
    await callback.message.answer(SECTIONS[callback.data])
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())