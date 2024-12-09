import json, certifi
import logging
import os
from datetime import datetime
from urllib.request import urlopen

import pandas as pd
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(name)s-%(levelname)s-%(message)s")
get_excel_df_logger = logging.getLogger("get_excel_df")
top_5_operations_logger = logging.getLogger("top_5_operations")
common_information_logger = logging.getLogger("common_information")
get_exchange_rate_logger = logging.getLogger("get_exchange_rate")
get_stock_price_logger = logging.getLogger("get_stock_price")


def get_excel_df(filename: str) -> list[dict]:
    """считывает данные из внешнего файла Excel и возвращает их в формате DataFrame
    за период с начала месяца до заданной даты в формате YYYY-MM-DD HH:MM:SS"""
    try:
        path = os.path.join("../data/", filename)
        excel_data = pd.read_excel(path)
        list_dict = excel_data.to_dict(orient="records")
        get_excel_df_logger.info(f"Успешное преобразование файла {filename} из объекта json в python")
        return list_dict
    except Exception as e:
        get_exchange_rate_logger.warning(
            f"!!!! Не удалось преобразовать файл {filename} из объекта json в python. Ошибка - {e}"
        )


def top_5_operations(list_dict: list[dict]) -> list:
    '''возвращает 5 самых крупных операции по столбцу "Сумма операции"'''
    try:
        list_data = []
        df = pd.DataFrame(list_dict)
        df["datetime"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        df_sorted = df.sort_values(by="Сумма платежа", ascending=False, inplace=False).iloc[0:5, :]
        for _, row in df_sorted.iterrows():
            dic = {}
            dic["date"] = row["Дата операции"]
            dic["card_number"] = row["Номер карты"]
            dic["amount"] = row["Сумма операции"]
            dic["category"] = row["Категория"]
            dic["descriprion"] = row["Описание"]
            list_data.append(dic)
        top_5_operations_logger.info("Успешно сформированы 5 самых доходных операций")
        return list_data[:6]
    except Exception as e:
        get_exchange_rate_logger.warning(
            f"""!!!! Не удалось сформировать отчет проверьте поля списка {list_dict}.
        Ошибка - {e}"""
        )
        return []


def common_information(list_dict: list[dict]) -> list:
    """возвращает общую информацию по всем транзакциям"""
    try:
        list_data = []
        df = pd.DataFrame(list_dict)
        df["datetime"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        grouped_data = df.groupby("Номер карты").agg({"Сумма платежа": "sum", "Кэшбэк": "sum"}).reset_index()
        grouped_data["Сумма платежа"] = grouped_data["Сумма платежа"].abs()
        for _, row in grouped_data.iterrows():
            dic = {}
            dic["last_digits"] = (row["Номер карты"])[-4:]
            dic["total_spent"] = row["Сумма платежа"]
            dic["cashbak"] = round((row["Кэшбэк"]) / (row["Сумма платежа"]) * 100, 2)
            list_data.append(dic)
        common_information_logger.info("Успешно сформированa общая информация по всем транзакциям")
        return list_data
    except Exception as e:
        get_exchange_rate_logger.warning(
            f"""!!!! Не удалось сформировать отчет проверьте поля списка {list_dict}.
        Ошибка - {e}"""
        )


def greetings():
    """возвращает привествие пользователю в зависимости от текущего времени суток"""
    date_obj = datetime.now()
    if 6 < date_obj.hour <= 10:
        return "Доброе утро!"
    elif 11 < date_obj.hour <= 16:
        return "Доброго дня!"
    elif 16 < date_obj.hour <= 21:
        return "Доброго вечера!"
    elif 21 < date_obj.hour <= 24 or 0 <= date_obj.hour <= 6:
        return "Доброй ночи!"


def get_exchange_rate(json_file) -> list:
    """получает json-файл с кодировкой иностранных валют и url-ссылку по обменным курсам валют и
    возвращает значения текущих котировок этих валют"""
    try:
        total_list = []
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        if response.status_code == 200:
            data_curr = response.json()
            with open((os.path.join("../data/", json_file)), "r") as file:
                user_shares = json.load(file)
                for i in user_shares["user_currencies"]:
                    dic = {}
                    dic["currency"] = i
                    dic["exchange_rate"] = data_curr["Valute"][i]["Value"]
                    total_list.append(dic)
            get_exchange_rate_logger.info(
                f'Успешно сформированы котировки {', '.join(user_shares["user_currencies"])} к рублю'
            )
            return total_list
    except Exception as e:
        get_exchange_rate_logger.warning(f"!!!! Не удалось отобразить котировки. Ошибка - {e}")
        return []


def get_stock_price(json_file: str) -> list:
    """получает json-файл с наименованиями ценных бумаг и url-ссылку на котировки ценных бумаг и
    возвращает их текущие котировки"""
    try:
        load_dotenv()
        API_key = os.getenv("API_KEY")
        total_list = []
        url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_key}"
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        stock_list = json.loads(data)
        with open((os.path.join("../data/", json_file)), "r") as file:
            user_shares = json.load(file)
        for i in user_shares["user_stocks"]:
            for q in stock_list:
                if i == q["symbol"]:
                    dic = {}
                    dic["stock"] = i
                    dic["price"] = q["price"]
                    total_list.append(dic)
        get_stock_price_logger.info(
            f'Успешно сформированы котировки акций {', '.join(user_shares["user_stocks"])} к рублю'
        )
        return total_list
    except Exception as e:
        get_stock_price_logger.warning(f"!!!! Не удалось отобразить котировки акции. Ошибка - {e}")
