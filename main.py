import os

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

import bot.handlers

# load local environment
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def auth(func):
    "Decorator for checking telegram user id"
    async def wrapper(message):
        if message['from']['id'] != CHAT_ID:
            return await message.answer("Access Denied")
        return await func(message)
    return wrapper


if __name__ == '__main__':
    exec(open("bot/handlers.py").read())
    executor.start_polling(dp, skip_updates=True)
