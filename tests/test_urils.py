import pytest,pandas as pd
from unittest.mock import Mock, patch, MagicMock
import datetime
from datetime import datetime
from src.utils import get_excel_df,top_5_operations,common_information,greetings,get_exchange_rate,get_stock_price


@pytest.fixture
def get_excel_return():
    return [{'Дата операции': '16.07.2019 16:30:10', 'Дата платежа': '18.07.2019', 'Номер карты': '*7197',
             'Статус': 'OK', 'Сумма операции':-49.8, 'Валюта операции':'RUB', 'Сумма платежа': -49.8,
 'Валюта платежа': 'RUB', 'Кэшбэк': 4, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'SPAR',
 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 49.8},
 {'Дата операции': '16.07.2019 16:13:54','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции':-114.0,'Валюта операции': 'RUB','Сумма платежа': -114.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 2,'Категория': 'Фастфуд','MCC': 5814.0,'Описание': 'IP Yakubovskaya M. V.','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 114.0},
 {'Дата операции': '16.07.2019 13:27:53','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции': -148.0,'Валюта операции': 'RUB','Сумма платежа': -148.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 10,'Категория': 'Транспорт','MCC': 4121.0,'Описание': 'Яндекс Такси','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 148.0}]

@patch('pandas.read_excel')
def test_get_excel_df_1(mock_get,get_excel_return):
    mock_get.return_value =pd.DataFrame([{'Дата операции': '16.07.2019 16:30:10', 'Дата платежа': '18.07.2019', 'Номер карты': '*7197',
             'Статус': 'OK', 'Сумма операции':-49.8, 'Валюта операции':'RUB', 'Сумма платежа': -49.8,
 'Валюта платежа': 'RUB', 'Кэшбэк': 4, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'SPAR',
 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 49.8},
 {'Дата операции': '16.07.2019 16:13:54','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции':-114.0,'Валюта операции': 'RUB','Сумма платежа': -114.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 2,'Категория': 'Фастфуд','MCC': 5814.0,'Описание': 'IP Yakubovskaya M. V.','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 114.0},
 {'Дата операции': '16.07.2019 13:27:53','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции': -148.0,'Валюта операции': 'RUB','Сумма платежа': -148.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 10,'Категория': 'Транспорт','MCC': 4121.0,'Описание': 'Яндекс Такси','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 148.0}])
    assert get_excel_df('filename.xlsx') == get_excel_return

@patch('pandas.read_excel')
def test_get_excel_df_2(mock_get):
    mock_get.return_value =pd.DataFrame({})
    assert get_excel_df('filename.xlsx') == []

@patch('src.utils.os.path.join')
def test_get_excel_df_3(mock_path,get_excel_return):
    mock_path.return_value = '../data/operations_test.xlsx'
    assert get_excel_df('operations_test.xlsx') == [{'MCC': 5411,'Бонусы (включая кэшбэк)': 3,'Валюта операции': 'RUB',
  'Валюта платежа': 'RUB','Дата операции': '31.12.2021 16:44:00','Дата платежа': '31.12.2021','Категория': 'Супермаркеты',
  'Кэшбэк': 2,'Номер карты': '*7197','Округление на инвесткопилку': 0,'Описание': 'Колхоз','Статус': 'OK',
  'Сумма операции': -160.89,'Сумма операции с округлением': 160.89,'Сумма платежа': -160.89},
 {'MCC': 5411,'Бонусы (включая кэшбэк)': 1,'Валюта операции': 'RUB','Валюта платежа': 'RUB',
  'Дата операции': '31.12.2021 16:42:04','Дата платежа': '31.12.2021','Категория': 'Супермаркеты','Кэшбэк': 4,
  'Номер карты': '*7197','Округление на инвесткопилку': 0,'Описание': 'Билла','Статус': 'OK','Сумма операции': -64.0,
  'Сумма операции с округлением': 64.0,'Сумма платежа': -64.0}]

@patch('os.path.join')
def test_get_excel_df_4(mock_path):
    mock_path.return_value = None
    assert get_excel_df('filename.xlsx') == None

def test_top_5_operations_1(get_excel_return):
    assert top_5_operations(get_excel_return) == [{'date': '16.07.2019 16:30:10', 'card_number': '*7197',
                                                   'amount': -49.8, 'category': 'Супермаркеты', 'descriprion': 'SPAR'},
                                                  {'date': '16.07.2019 16:13:54', 'card_number': '*7197',
                                                   'amount': -114.0, 'category': 'Фастфуд',
                                                   'descriprion': 'IP Yakubovskaya M. V.'},
                                                  {'date': '16.07.2019 13:27:53', 'card_number': '*7197',
                                                   'amount': -148.0, 'category': 'Транспорт',
                                                   'descriprion': 'Яндекс Такси'}]


def test_top_5_operations_2(get_excel_return):
    assert top_5_operations(None) == []



def test_common_information_1(get_excel_return):
    assert common_information(get_excel_return) == [{'last_digits': '7197', 'total_spent': 311.8, 'cashbak': 5.13}]

def test_common_information_2():
    assert common_information([]) == None

def test_common_information_3():
    assert common_information(None) == None

def test_common_information_4():
    assert common_information(None) == None


# def test_common_information_5(get_excel_return):
#     mock_get = Mock(return_value=get_excel_return)
#     pd.DataFrame =  mock_get
#     assert common_information(get_excel_return) == None


@patch('src.utils.datetime')
def test_greetings_1 (mock_datetime):
    mock_datetime.now.return_value = datetime(2024,2,12,14,20,55)
    assert greetings () == "Доброго дня!"

@patch('src.utils.datetime')
def test_greetings_2(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 2, 12, 20, 20, 55)
    assert greetings() == "Доброго вечера!"

@patch('src.utils.datetime')
def test_greetings_3(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 2, 12, 2, 20, 55)
    assert greetings() == "Доброй ночи!"

@patch('src.utils.datetime')
def test_greetings_4(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 2, 12, 7, 20, 55)
    assert greetings() == "Доброе утро!"
    # def greetings():
    #     """возвращает привествие пользователю в зависимости от текущего времени суток"""
    #     date_obj = datetime.now()
    #     if 6 < date_obj.hour <= 10:
    #         return "Доброе утро!"
    #     elif 11 < date_obj.hour <= 16:
    #         return "Доброго дня!"
    #     elif 16 < date_obj.hour <= 21:
    #         return "Доброго вечера!"
    #     elif 21 < date_obj.hour <= 6:
    #         return "Доброй ночи!"



@patch('requests.get')
def test_get_exchange_rate_1(mock_get):
    mock_get.return_value.json.return_value = {'Valute': {
'USD': {'ID': 'R01235', 'NumCode': '840', 'CharCode': 'USD', 'Nominal': 1, 'Name': 'Доллар США', 'Value': 99.4215, 'Previous': 103.3837},
'EUR': {'ID': 'R01239', 'NumCode': '978', 'CharCode': 'EUR', 'Nominal': 1, 'Name': 'Евро', 'Value': 106.304, 'Previous': 109.7802},
'CNY': {'ID': 'R01375', 'NumCode': '156', 'CharCode': 'CNY', 'Nominal': 1, 'Name': 'Китайский юань', 'Value': 13.597, 'Previous': 14.1399},
'TRY': {'ID': 'R01700J', 'NumCode': '949', 'CharCode': 'TRY', 'Nominal': 10, 'Name': 'Турецких лир', 'Value': 28.6464, 'Previous': 29.7777}}}
    mock_get.return_value.status_code = 200
    assert get_exchange_rate('user_settings.json') == [{'currency': 'USD', 'exchange_rate': 99.4215},
                                                     {'currency': 'CNY', 'exchange_rate': 13.597},
                                                     {'currency': 'EUR', 'exchange_rate': 106.304},
                                                     {'currency': 'TRY', 'exchange_rate': 28.6464}]


def test_get_exchange_rate_2():
    assert get_exchange_rate('user_settings.json') == [{'currency': 'USD', 'exchange_rate': 99.3759},
 {'currency': 'CNY', 'exchange_rate': 13.524},
 {'currency': 'EUR', 'exchange_rate': 105.0996},
 {'currency': 'TRY', 'exchange_rate': 28.6122}]


def test_get_exchange_rate_3():
    assert get_exchange_rate('filename.json') == []

@patch('urllib.request.urlopen')
def test_get_stock_price(mock_get):
    mock_get.return_value.read.return_value.decode("utf-8").return_value =[{"symbol": "SADL","price": 18.25,"exchange": "New York Stock Exchange"},{"symbol": "AMZN","price": 227.03,"exchange": "New York Stock Exchange"},{"symbol": "IBACU","price": 98.32,"exchange": "New York Stock Exchange"}]

    assert get_stock_price('user_settings.json') == [{'price': 18.25, 'stock': 'SADL'},
                                                     {'price': 226.09, 'stock': 'AMZN'},
                                                     {'price': 1.12, 'stock': 'REUN'},
                                                     {'price': 446.02, 'stock': 'MSFT'},
                                                     {'price': 389.79, 'stock': 'TSLA'},
                                                     {'price': 10.05, 'stock': 'IBACU'}]


