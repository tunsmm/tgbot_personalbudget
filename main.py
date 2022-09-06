import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import aiohttp

from utils.categories import Categories
from utils.stats import get_current_week_stats, get_current_year_stats, get_today_stats, get_current_month_stats, get_yesterday_stats, get_custom_stats
import utils.exceptions as exceptions
import utils.expenses as expenses
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
