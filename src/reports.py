import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO, format="%(levelname)s-%(message)s")
spending_by_weekday_logger = logging.getLogger("spending_by_weekday")


def print_spending_by_date(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open(os.path.join("./print_decorators/report_1.txt"), "w"):
            return result.to_string(buf="report_1.txt", header=False)
    return wrapper


def print_name_spending_by_date(file_name):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(os.path.join(f"./print_decorators/{file_name}"), "w"):
                return result.to_string(buf=file_name, header=False)
        return wrapper
    return my_decorator


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> str:
    """возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)"""
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%Y-%m-%d")

        transactions["datetime"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        transactions["day_name"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True).dt.day_name()
        df = transactions[
            (transactions["datetime"] >= (date + relativedelta(months=-3))) & (transactions["datetime"] <= date)
        ].groupby(by="day_name")
        print(df.head(10))
        spending_by_weekday_logger.info("Успешное формирование отчета о средних тратах.")
        return (df["Сумма платежа"].mean().abs().round(2)).to_json()
    except Exception as e:
        spending_by_weekday_logger.warning(f"!!!! Неудачное формирование отчета. Ошибка - {e}")
