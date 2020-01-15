import datetime
import re
from typing import NamedTuple, List, Dict

import pytz

import db
import exceptions
from categories import Categories


class Expense(NamedTuple):
    amount: int
    category_name: str


class Message(NamedTuple):
    amount: int
    category_text: str


def _parse_message(input_message):
    regexp_result = re.match(r"([\d ]+) (.*)", input_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.InvalidMessage(
            "Sorry, don't understand the message. "
            "Please enter is in the following format: "
            "\n200 taxi")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d")


def _get_now_datetime():
    """Return date time with respect to timezone Tallinn"""
    tz = pytz.timezone("Europe/Tallinn")
    now = datetime.datetime.now(tz)
    return now


def add_expense(input_message: str) -> Expense:
    parsed_message = _parse_message(input_message)
    category = Categories().get_category(
        parsed_message.category_text)
    if category:
        db.insert("expense", {
            "amount": parsed_message.amount,
            "created": _get_now_formatted(),
            "category_codename": category.codename,
            "raw_text": input_message
        })
        return Expense(amount=parsed_message.amount, category_name=category.name)
    else:
        raise exceptions.CategoryNotDefined(f'Unfortunately you cannot submit an expense for category '
                                            f'{parsed_message.category_text}. \n'
                                            f'You can check what expense categories available by sending /categories'
                                            f'to me')


def get_remaining_budget() -> float:
    cursor = db.get_cursor()
    cursor.execute("select sum(e.amount) "
                   "from expense e left join category c "
                   "on c.codename=e.category_codename "
                   "where c.inside_budget = true ")
    result = cursor.fetchone()
    result = result[0] if result[0] else 0
    cursor.execute(f"select budget_amount from budget")
    total_budget = cursor.fetchone()
    total_budget = total_budget[0] if total_budget[0] else 0
    remaining_budget = float(total_budget) - float(result)
    return remaining_budget


def get_all_expenses_inside_budget():
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name "
        "from expense e left join category c "
        "on c.codename=e.category_codename "
        "where c.inside_budget = true "
        "order by created desc")
    rows = cursor.fetchall()
    expenses_in_budget = []
    for row in rows:
        print(row)
        expenses_in_budget.append({
            'amount': row[1],
            'id': row[0],
            'category_name': row[2]
        })
    return expenses_in_budget


def get_all_expenses_outside_budget():
    """Returns expenses outside of budget"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name "
        "from expense e left join category c "
        "on c.codename=e.category_codename "
        "where c.inside_budget = false "
        "order by created desc")
    rows = cursor.fetchall()
    expenses_outside_budget = []
    for row in rows:
        expenses_outside_budget.append({
            'amount': row[1],
            'id': row[0],
            'category_name': row[2]
        })
    return expenses_outside_budget


def last():
    """Returns a few last expenses"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name, e.created "
        "from expense e left join category c "
        "on c.codename=e.category_codename "
        "order by created desc limit 10")
    rows = cursor.fetchall()
    last_expenses = []
    for row in rows:
        last_expenses.append({
            'amount': row[1],
            'id': row[0],
            'category_name': row[2]
        })
    return last_expenses


def get_total_budget():
    cursor = db.get_cursor()
    cursor.execute(
        "select budget_amount from budget")
    result = cursor.fetchone()
    return result[0]
