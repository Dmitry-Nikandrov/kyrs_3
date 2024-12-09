import datetime
import json
import logging
from typing import Union

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(levelname)s-%(levelname)s-%(message)s")
get_excel_list_logger = logging.getLogger("get_excel_list")
most_profit_cashback_logger = logging.getLogger("most_profit_cashback")
invest_bank_logger = logging.getLogger("invest_bank")


def most_profit_cashback(transactions: list[dict], year, month: Union[int, str]) -> str:
    """возвращает повышенные категории кэшбека из списка транзакций за определенные месяц и год"""
    try:
        if int(month) < 1 or int(month) > 12:
            most_profit_cashback_logger.warning(
                f"!!!! Проверьте корректность номера месяца. Текущее значение месяца - {month}"
            )
            return "[]"
        elif not transactions:
            most_profit_cashback_logger.warning(
                "!!!! Список словарей должен содержать значения. Список словарей не содержит данных"
            )
            return "[]"
        else:
            data = pd.DataFrame(transactions)
            data["datetime"] = pd.to_datetime(data["Дата операции"], dayfirst=True)
            df = data[(data["datetime"].dt.year == year) & (data["datetime"].dt.month == month)]
            data_gr = df.groupby(by="Категория").agg({"Кэшбэк": "sum"})

            final_list = []
            df_final = (
                data_gr[data_gr["Кэшбэк"] != 0].sort_values(by="Кэшбэк", inplace=False, ascending=False).reset_index()
            )
            for _, row in df_final.iterrows():
                dic = {}
                key = f"Категория {row['Категория']}"
                dic[key] = row["Кэшбэк"]
                final_list.append(dic)
            most_profit_cashback_logger.info(
                f"Успешно сформированы данные о повышенных категориях кэшбека за {month} месяц {year} года"
            )
            return json.dumps(final_list, ensure_ascii=False)
    except Exception as e:
        most_profit_cashback_logger.warning(
            f"""!!!! Не удалось формированы данные о повышенных категориях кэшбека.
        Ошибка - {e}"""
        )
        return "[]"


def invest_bank(transactions: list[dict], month: str, limit: int) -> float:
    """Возвращает сумму денежных средств, которую можно отложить с трат при заданном размере округления"""
    try:
        if not transactions:
            invest_bank_logger.warning('!!!! Список словарей должен содержать значения.')
        elif limit < 0:
            invest_bank_logger.warning(
                f"!!!! Проверьте корректность порога округления месяца. Текущее значение месяца - {limit}"
            )
        else:
            data = pd.DataFrame(transactions)
            data["datetime"] = pd.to_datetime(data["Дата операции"], dayfirst=True)
            data_obj = datetime.datetime.strptime(month, "%Y-%m")
            data["datetime_new"] = data["datetime"].dt.strftime("%y-%m")
            df_init = data[(data["datetime"].dt.year == data_obj.year) & (data["datetime"].dt.month == data_obj.month)]
            if df_init.empty:
                invest_bank_logger.info("Задайте другую дату")
            else:
                pd.options.mode.chained_assignment = None  # default='warn'
                df_init["Платеж_округл"] = df_init["Сумма платежа"].round(-2).abs()
                df = df_init[df_init["Сумма платежа"] < 0]
                df["Сумма платежа"] = -df["Сумма платежа"]
                df["Инвесткопилка"] = ((df["Сумма платежа"] / limit).apply(np.ceil)) * limit - df["Сумма платежа"]
                invest_bank_logger.info(f"На инвесткопилку можно отложить {round(df['Инвесткопилка'], 2).sum()} д.ед.")
                return float(round(df["Инвесткопилка"], 2).sum())
    except Exception as e:
        invest_bank_logger.warning(f"!!!! Неудачное завершение операции. Ошибка {e}.")
