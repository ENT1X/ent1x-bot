import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, ADMIN_ID

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан! Добавь переменную окружения в Railway.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


MINIAPP_URL = "https://ent1x.github.io/ent1x-bot/miniapp.html"


def main_kb() -> ReplyKeyboardMarkup:
    webapp = WebAppInfo(url=MINIAPP_URL)
    btn = KeyboardButton(text="Открыть заявку", web_app=webapp)
    return ReplyKeyboardMarkup(
        keyboard=[[btn]],
        resize_keyboard=True,
    )


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        "Привет! Я ENT1X 👋\n\n"
        "Через это мини-приложение ты можешь оставить заявку на разработку:\n"
        "— Сайт под ключ\n"
        "— Интернет-магазин\n"
        "— Telegram бот\n\n"
        "Просто нажми кнопку ниже 👇"
    )
    await message.answer(text, reply_markup=main_kb())


@dp.message()
async def webapp_data_handler(message: types.Message):
    if not message.web_app_data:
        return

    try:
        data = json.loads(message.web_app_data.data)
    except json.JSONDecodeError:
        await message.answer("Ошибка: не удалось обработать данные.")
        return

    name = data.get("name", "—")
    contact = data.get("contact", "—")
    service = data.get("service", "—")
    desc = data.get("desc", "—")

    user_info = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
    user_link = f"tg://user?id={message.from_user.id}"

    answer_text = (
        f"✅ Заявка принята!\n\n"
        f"Услуга: {service}\n"
        f"Имя: {name}\n"
        f"Контакты: {contact}\n"
        f"Описание: {desc}\n\n"
        f"Я свяжусь с вами в ближайшее время."
    )
    await message.answer(answer_text)

    if ADMIN_ID:
        admin_text = (
            f"📩 Новая заявка из Mini App\n\n"
            f"Пользователь: <a href=\"{user_link}\">{user_info}</a>\n"
            f"Имя: {name}\n"
            f"Контакт: {contact}\n"
            f"Услуга: {service}\n"
            f"Описание: {desc}"
        )
        try:
            await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
        except Exception as e:
            logging.warning(f"Не удалось отправить уведомление админу: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
