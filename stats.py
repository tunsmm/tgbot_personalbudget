from datetime import date, datetime, timezone, timedelta

import db


def get_period_stats(codename: str, mode: str, day_from: date, day_to: date) -> str:
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   f"from expense where created >= '{day_from}'"
                   f"and created <= '{day_to}'")
    result = cursor.fetchone()
    if not result[0]:
        return f"No expenses {codename}"
    all_expenses = result[0]
    
    if mode == "short": 
        return (f"Expenses {codename}:\n"
            f"total — {all_expenses}\n"
            f"See full stats: /{codename}")
    elif mode == "full":
        cursor.execute("select sum(amount) "
                    f"from expense where created >= '{day_from}' "
                    f"and created <= '{day_to}' "
                    "and category_codename in (select codename "
                    "from category where is_base_expense=true)")
        result = cursor.fetchone()
        base_expenses = result[0] if result[0] else 0
        return (f"Expenses {codename}:\n"
                f"total — {all_expenses}\n"
                f"basic — {base_expenses} from {_get_budget_limit()}\n\n"
                f"See general stats: /stats")
    else: 
        return "Unexpected mode"


def get_today_stats(mode: str) -> str:
    return get_period_stats("today", mode, _get_now_formatted(), _get_now_formatted())


def get_yesterday_stats(mode: str) -> str:
    now = _get_now_datetime()
    yesterday = f'{now.year:04d}-{now.month:02d}-{(now.day-1):02d}'
    return get_period_stats("yesterday", mode, yesterday, yesterday)    


def get_current_week_stats(mode: str) -> str:
    now = _get_now_datetime()
    monday = now - timedelta(days = now.weekday())
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = f'{monday.year:04d}-{monday.month:02d}-{monday.day:02d}'
    return get_period_stats("week", mode, monday, _get_now_formatted())


def get_current_month_stats(mode: str) -> str:
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    return get_period_stats("month", mode, first_day_of_month, _get_now_formatted())


def get_current_year_stats(mode: str) -> str:
    now = _get_now_datetime()
    first_day_of_year = f'{now.year:04d}-01-01'
    return get_period_stats("year", mode, first_day_of_year, _get_now_formatted())


def get_custom_stats(date1, date2) -> str:
    date_from = f'{date1.year:04d}-{date1.month:02d}-{date1.day:02d}'
    date_to = f'{date2.year:04d}-{date2.month:02d}-{date2.day:02d}'
    return get_period_stats(f"period from {date_from} to {date_to}", "full", date_from, date_to)


def _get_budget_limit() -> int:
    return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d")


def _get_now_datetime() -> date:
    timezone_offset = +3.0  
    tzinfo = timezone(timedelta(hours=timezone_offset))
    now = datetime.now(tzinfo)
    return now
