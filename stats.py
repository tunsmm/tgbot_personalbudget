from datetime import date, datetime, timezone, timedelta

import db


def get_general_stats() -> str:
    return get_today_stats() + "\n\n" + get_month_stats()


def get_today_stats() -> str:
    now = _get_now_datetime()
    today_day = f'{now.year:04d}-{now.month:02d}-{now.day:02d}'
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   f"from expense where created='{today_day}'")
    result = cursor.fetchone()
    if not result[0]:
        return "No expenses today"
    all_today_expenses = result[0]
    cursor.execute("select sum(amount) "
                   f"from expense where created='{today_day}' "
                   "and category_codename in (select codename "
                   "from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    return (f"Today's expenses:\n"
            f"total — {all_today_expenses}\n"
            f"basic — {base_today_expenses} from {_get_budget_limit()}\n\n"
            f"Current month: /month")


def get_month_stats() -> str:
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) "
                   f"from expense where created >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "No expenses in this month"
    all_month_expenses = result[0]
    cursor.execute(f"select sum(amount) "
                   f"from expense where created >= '{first_day_of_month}' "
                   f"and category_codename in (select codename "
                   f"from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_month_expenses = result[0] if result[0] else 0
    return (f"Month's expenses:\n"
            f"total — {all_month_expenses}\n"
            f"basic — {base_month_expenses} from "
            f"{now.day * _get_budget_limit()}"
            f"Current day: /today")


def _get_all_expenses(period) -> int:
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) "
                   f"from expense where created >= '{period}'")
    result = cursor.fetchone()
    if not result[0]:
        return "No expenses in this period"
    all_month_expenses = result[0]
    return 0

def _get_budget_limit() -> int:
    return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d")


def _get_now_datetime() -> date:
    timezone_offset = +3.0  
    tzinfo = timezone(timedelta(hours=timezone_offset))
    now = datetime.now(tzinfo)
    return now
