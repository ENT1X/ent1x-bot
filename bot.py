import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)

from config import BOT_TOKEN

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан! Добавь переменную окружения в Railway.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

MINIAPP_URL = "https://ent1x.github.io/ent1x-bot/miniapp.html"


def main_kb() -> ReplyKeyboardMarkup:
    webapp = WebAppInfo(url=MINIAPP_URL)
    btn = KeyboardButton(text="📋 Услуги и цены", web_app=webapp)
    return ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        "Привет! Я ENT1X 👋\n\n"
        "Создаю сайты, интернет-магазины и Telegram "
        "ботов под ключ.\n\n"
        "Нажми кнопку ниже, чтобы посмотреть услуги "
        "и написать мне."
    )
    await message.answer(text, reply_markup=main_kb())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
