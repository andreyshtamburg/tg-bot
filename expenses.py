import re
from typing import NamedTuple, List

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


def add_expense(input_message: str) -> Expense:
    parsed_message = _parse_message(input_message)
    category = Categories().getCategory


