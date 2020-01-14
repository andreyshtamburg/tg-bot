import logging
import os

from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
from middlewares import AccessMiddleware

ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Send welcome message and help"""
    await message.answer(
        "Hey! I'm Topia expense tracking bot\n\n"
        "Add an Expense: 250 uber\n"
        "Today's statistic: /today\n"
        "Current month statistics: /month\n"
        "Latest expenses: /expenses\n"
        "Categories: /categories\n"
        "Remaining budget: /remaining")


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Send a few last expenses"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("No expenses added yet")
        return

    last_expenses_rows = [
        f"{row['amount']} EUR on {row['category_name']}"
        for row in last_expenses]
    answer_message = "Last expenses:\n\n* " + "\n\n* ".join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler(commands=['remaining'])
async def remaining_budget(message: types.Message):
    answer_message = str(expenses.get_remaining_budget()) + " EUR"
    await message.answer(answer_message)


@dp.message_handler(commands=['summary'])
async def budget_summary(message: types.Message):
    total_budget = expenses.get_total_budget()
    remaining = expenses.get_remaining_budget()
    inside_budget = expenses.get_all_expenses_inside_budget()
    inside_budget_rows = [f"{row['amount']} EUR on {row['category_name']}"
                          for row in inside_budget]
    outside_budget = expenses.get_all_expenses_outside_budget()
    outside_budget_rows = [f"{row['amount']} EUR on {row['category_name']}"
                           for row in outside_budget]
    #   FIXME file is too large ???? it's a fucking text ????
    total_budget_message = f'Your total budget is *{total_budget} EUR*\n'
    remaining_budget_message = f'Your remaining budget is *{remaining} EUR*\n'
    expenses_inside_budget_message = "Expenses inside budget are :\n\n* " + "\n\n* ".join(inside_budget_rows) + "\n\n"
    expenses_outside_budget_message = "Expenses outside budget are:\n\n* " + "\n\n* ".join(outside_budget_rows)
    answer_message = total_budget_message + remaining_budget_message + expenses_inside_budget_message + \
                     expenses_outside_budget_message

    # answer_message = f'''Your total budget is *{total_budget} EUR*\n
    #                      Your remaining budget is *{remaining} EUR*\n'''.join(
    #                     "Expenses inside budget are :\n\n* " + "\n\n* ".join(inside_budget_rows)).join(
    #                     "Expenses outside budget are:\n\n* " + "\n\n* ".join(outside_budget_rows))

    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Adds new expense"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.InvalidMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Added expense {expense.amount} EUR for {expense.category_name}.\n\n"
        f"Remaining budget is {expenses.get_remaining_budget()} EUR")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
