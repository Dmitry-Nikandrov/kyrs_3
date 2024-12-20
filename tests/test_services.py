from src.services import most_profit_cashback, invest_bank

from tests.test_urils import get_excel_return

def test_most_profit_cashback_1():
    assert (most_profit_cashback([{'Дата операции': '16.07.2019 16:30:10', 'Дата платежа': '18.07.2019',
    'Номер карты': '*7197','Статус': 'OK', 'Сумма операции':-49.8, 'Валюта операции':'RUB','Сумма платежа': -49.8,
 'Валюта платежа': 'RUB', 'Кэшбэк': 4, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'SPAR',
 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 49.8},
 {'Дата операции': '16.07.2019 16:13:54','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции':-114.0,'Валюта операции': 'RUB','Сумма платежа': -114.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 2,'Категория': 'Фастфуд','MCC': 5814.0,'Описание': 'IP Yakubovskaya M. V.','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 114.0},
 {'Дата операции': '16.07.2019 13:27:53','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции': -148.0,'Валюта операции': 'RUB','Сумма платежа': -148.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 10,'Категория': 'Транспорт','MCC': 4121.0,'Описание': 'Яндекс Такси','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 148.0}],2019,7)==
'[{"Категория Транспорт": 10}, {"Категория Супермаркеты": 4}, {"Категория Фастфуд": 2}]')

def test_most_profit_cashback_2():
    assert (most_profit_cashback([{}], 2019,7)) == '[]'

def test_most_profit_cashback_3():
    assert (most_profit_cashback(None, 2019,14)) == '[]'

def test_most_profit_cashback_4():
    assert (most_profit_cashback(None, 2019,14)) == '[]'


def test_invest_bank_1():
    assert invest_bank([{'Дата операции': '16.07.2019 16:30:10', 'Дата платежа': '18.07.2019',
    'Номер карты': '*7197','Статус': 'OK', 'Сумма операции':-49.8, 'Валюта операции':'RUB','Сумма платежа': -49.8,
 'Валюта платежа': 'RUB', 'Кэшбэк': 4, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'SPAR',
 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 49.8},
 {'Дата операции': '16.07.2019 16:13:54','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции':-114.0,'Валюта операции': 'RUB','Сумма платежа': -114.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 2,'Категория': 'Фастфуд','MCC': 5814.0,'Описание': 'IP Yakubovskaya M. V.','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 114.0},
 {'Дата операции': '16.07.2019 13:27:53','Дата платежа': '17.07.2019','Номер карты': '*7197','Статус': 'OK',
  'Сумма операции': -148.0,'Валюта операции': 'RUB','Сумма платежа': -148.0,'Валюта платежа': 'RUB',
  'Кэшбэк': 10,'Категория': 'Транспорт','MCC': 4121.0,'Описание': 'Яндекс Такси','Бонусы (включая кэшбэк)': 2,
  'Округление на инвесткопилку': 0,'Сумма операции с округлением': 148.0}],'2019-07',30) == 18.2

def test_invest_bank_2():
    assert invest_bank([{}],'2019-07',30) == None

def test_invest_bank_3():
    assert invest_bank([{}],'2024-15',0.22) == None

def test_invest_bank_4():
    assert invest_bank(None,'2024-15',-2) == None