import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from categories import Categories
import exceptions
import expenses

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def auth(func):
    "Decorator for checking telegram user id"
    async def wrapper(message):
        if message['from']['id'] != CHAT_ID:
            return await message.reply("Access Denied", reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(commands=['start', 'help'])
@auth
async def send_welcome(message: types.Message):
    "Welcome message"
    await message.reply(
        "Bot for budgeting\n\n"
        "Add expenses: 250 taxi\n"
        "Last expenses: /expenses\n"
        "Categories of expenses: /categories",
        reply=False)


@dp.message_handler(commands=['expenses'])
@auth
async def list_expenses(message: types.Message):
    last_expenses = expenses.last()
    if not last_expenses:
        await message.reply("No expenses", reply=False)
        return

    last_expenses_rows = [
        f"{row['amount']} on {row['category_name']} —  click "
        f"/del{row['id']} for delete"
        for row in last_expenses]
    answer_message = "Last expenses:\n\n* " + "\n\n* ".join(last_expenses_rows)
    await message.reply(answer_message, reply=False)


@dp.message_handler(lambda message: message.text.startswith('/del'))
@auth
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Deleted"
    await message.reply(answer_message, reply=False)


@dp.message_handler()
@auth
async def add_expense(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.reply(str(e), reply=False)
        return
    answer_message = (
        f"Added expenses {expense.amount} on {expense.category_name}.\n\n")
    await message.reply(answer_message, reply=False)


@dp.message_handler(commands=['categories'])
@auth
async def categories_list(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Categories of expenses:\n\n* " +\
            ("\n* ".join([c["name"]+' ('+", ".join(c["aliases"])+')' for c in categories]))
    await message.reply(answer_message, reply=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)