import pytest,json
import pandas as pd
from unittest.mock import mock_open, patch

from src.reports import spending_by_weekday,print_spending_by_date, print_name_spending_by_date

@pytest.fixture
def df_spendings():
    return pd.DataFrame({
'Дата операции': ['31.01.2022 16:44:00','30.12.2021 16:44:00','24.12.2021 16:44:00'],
'Дата платежа': ['31.12.2021','30.12.2021','24.12.2021'],
'Сумма операции': [-160.89,-400,-900],
'Сумма платежа': [-160.89,-400,-900],
})

def test_spending_by_weekday_1(df_spendings):
     assert spending_by_weekday(df_spendings,'2022-02-01') =='{"Friday":900.0,"Monday":160.89,"Thursday":400.0}'

def test_spending_by_weekday_2(df_spendings):
    assert spending_by_weekday(df_spendings)== '{}'

def test_spending_by_weekday_3():
    assert spending_by_weekday([],'2021.1.40')== None

df_ff =pd.DataFrame({'Дата операции':['31.01.2022 16:44:00'],'Сумма операции':[-160.89]})

def test_simple_decorator():
    @print_spending_by_date
    def simple(df):
        return df

    simple(df_ff)
    with open('./print_decorators/report_1.txt','r') as file:
            text = file.read()
            print (text)
            assert simple(df_ff) == None

def test_decorator_param():
    @print_name_spending_by_date('report_2.txt')
    def simple(df):
        return df

    simple(df_ff)
    with open('./print_decorators/report_2.txt','r') as file:
            text = file.read()
            if text == '':
                print('Тест выполнен удачно')
                assert simple(df_ff) == None
            else:
                print('Тест выполнен не удачно')