import asyncio
import os
import json
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    MenuButtonDefault,
)
from aiogram.filters import CommandStart, Command

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

WEBAPP_URL = "https://ai64ka.github.io/yzoridushi_bot/"
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


def init_db():
    conn = sqlite3.connect("orders.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            item TEXT,
            price TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_order(user_id, username, item, price):
    conn = sqlite3.connect("orders.db")
    conn.execute(
        "INSERT INTO orders (user_id, username, item, price, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, item, price, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🎨 Открыть витрину", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
    )


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Это бот Daniel Ramo 🎨\n\n"
        "Нажми «Открыть витрину», выбери работу или услугу и оставь заявку:",
        reply_markup=main_keyboard(),
    )


@dp.message(Command("id"))
async def get_id(message: Message):
    await message.answer(f"Твой Telegram ID: {message.from_user.id}")


@dp.message(F.web_app_data)
async def on_order(message: Message):
    data = json.loads(message.web_app_data.data)
    item = data.get("item", "—")
    price = data.get("price", "—")
    user = message.from_user

    save_order(user.id, user.username, item, price)

    await message.answer(
        f"Спасибо! Заявка принята ✅\n\n{item} — {price}\n"
        "Художница скоро свяжется с тобой."
    )

    if ADMIN_ID:
        who = f"@{user.username}" if user.username else user.full_name
        await bot.send_message(
            ADMIN_ID,
            f"🔔 Новая заявка!\n\n{item} — {price}\nОт: {who} (id {user.id})",
        )


async def main():
    init_db()
    await bot.set_chat_menu_button(menu_button=MenuButtonDefault())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())