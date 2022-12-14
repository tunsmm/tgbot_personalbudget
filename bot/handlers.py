from aiogram import types
import aiohttp

from main import auth, dp
from utils.categories import Categories
import utils.stats as stats
import utils.exceptions as exceptions
import utils.expenses as expenses


@dp.message_handler(commands=['start', 'help'])
@auth
async def send_welcome(message: types.Message):
    "Welcome message"
    await message.answer(
        "Bot for budgeting\n\n"
        "Add expenses: 250 taxi\n"
        "Last expenses: /expenses\n"
        "Categories of expenses: /categories\n"
        "Statistics: /stats")


@dp.message_handler(commands=['expenses'])
@auth
async def list_expenses(message: types.Message):
    """Return list of last 10 expenses"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("No expenses")
        return

    last_expenses_rows = [
        f"{row['amount']} on {row['category_name']} —  click "
        f"/del{row['id']} for delete"
        for row in last_expenses]
    answer_message = "Last expenses:\n\n* " + "\n\n* ".join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
@auth
async def categories_list(message: types.Message):
    """Return list of categories"""
    categories = Categories().get_all_categories()
    answer_message = "Categories of expenses:\n\n* " +\
            ("\n* ".join([c["name"]+' ('+", ".join(c["aliases"])+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['stats'])
@auth
async def show_stats(message: types.Message):
    """Return basic stats information. Includes stats for today, yesterday, week, month, year"""
    answer_message = f"""
                            {stats.get_today_stats("short")} 
                        \n{stats.get_yesterday_stats("short")} 
                        \n{stats.get_current_week_stats("short")} 
                        \n{stats.get_current_month_stats("short")}
                        \n{stats.get_current_year_stats("short")}
                        \nFor more information you can write /help_stats
                      """
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
@auth
async def today_stats(message: types.Message):
    """Return stats for today"""
    answer_message = stats.get_today_stats("full")
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
@auth
async def month_stats(message: types.Message):
    """Return stats for month"""
    answer_message = stats.get_current_month_stats("full")
    await message.answer(answer_message)


@dp.message_handler(commands=['yesterday'])
@auth
async def yesterday_stats(message: types.Message):
    """Return stats for yesterday"""
    answer_message = stats.get_yesterday_stats("full")
    await message.answer(answer_message)


@dp.message_handler(commands=['week'])
@auth
async def week_stats(message: types.Message):
    """Return stats for week"""
    answer_message = stats.get_current_week_stats("full")
    await message.answer(answer_message)


@dp.message_handler(commands=['year'])
@auth
async def year_stats(message: types.Message):
    """Return stats for year"""
    answer_message = stats.get_current_year_stats("full")
    await message.answer(answer_message)


@dp.message_handler(commands=['custom_stats'])
@auth
async def custom_stats(message: types.Message):
    """Return custom stats between two periods that user send in the message after the command. 
    It should be looks like: /custom stats 30012021 15072021
    where first two numbers of each period are days
    second two numbers are months
    last four numbers are years 
    """
    answer_message = stats.get_custom_stats(message.text)
    await message.answer(answer_message)


@dp.message_handler(commands=['help_stats'])
@auth
async def help_stats(message: types.Message):
    """Return help information about stats section"""
    await message.reply(
        "Help stats\n"
        "To see more information about any period just write some of these words: "
        "/today, /yesterday, /week, /month, /year\n"
        "Also you can write /custom_stats and add two date at this command to return stats", 
        reply=False)


@dp.message_handler(lambda message: message.text.startswith('/del'))
@auth
async def del_expense(message: types.Message):
    """Delete certain row of expenses by its id"""
    row_id = int(message.text[4:]) # text like /del{int}
    expenses.delete_expense(row_id)
    answer_message = "Deleted"
    await message.answer(answer_message)


@dp.message_handler()
@auth
async def add_expense(message: types.Message):
    "Add new expense"
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Added expenses {expense.amount} on {expense.category_name}.\n\n")
    await message.answer(answer_message)
