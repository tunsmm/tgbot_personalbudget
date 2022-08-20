from typing import NamedTuple

from categories import Categories
from messages import parse_message
from stats import _get_now_formatted
import db


class Expense(NamedTuple):
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    parsed_message = parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text)
    inserted_row_id = db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category["codename"],
        "raw_text": raw_message
    })
    return Expense(amount=parsed_message.amount,
                   category_name=category["name"])


def last():
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name "
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


def delete_expense(row_id: int) -> None:
    db.delete("expense", row_id)
