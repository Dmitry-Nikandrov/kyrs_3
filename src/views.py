import pandas as pd
import os,requests,json, certifi
from datetime import  datetime
from urllib.request import urlopen
from pandas.core.interchange.dataframe_protocol import DataFrame


def get_excel (filename):
    '''считывает данные из внешнего файла Excel и возвращает их в формате DataFrame'''
    path = os.path.join('../data/',filename)
    excel_data = pd.read_excel(path)
    excel_df = pd.DataFrame(excel_data)
    return excel_df

json_data = get_excel('operations.xlsx')

def top_5_operations(df:DataFrame)->DataFrame:
    '''возвращает 5 самых крупных операции по столбцу "Сумма операции"'''
    list_data =[]
    df_sorted=df.sort_values(by = 'Сумма платежа',ascending=False,inplace=False).iloc[0:5, :]
    #df_top_5 = df_sorted.to_dict(orient='records')
    for _,row in df_sorted.iterrows():
        dic = {}
        dic['date'] = row['Дата операции']
        dic['card_number'] = row['Номер карты']
        dic['amount'] = row ['Сумма операции']
        dic['category'] = row['Категория']
        dic['descriprion'] = row['Описание']
        list_data.append(dic)
    return list_data[:6]


def common_information(df: DataFrame) -> list:
    '''возвращает общую информацию по всем транзакциям '''
    list_data = []
    grouped_data = df.groupby('Номер карты').agg({'Сумма платежа':sum,'Кэшбэк':sum}).reset_index()
    grouped_data['Сумма платежа'] = grouped_data['Сумма платежа'].abs()
    for _, row in grouped_data.iterrows():
        dic = {}
        dic['last_digits'] = (row['Номер карты'])[-4:]
        dic['total_spent'] = row['Сумма платежа']
        dic["cashbak"] = round((row['Кэшбэк'])/(row['Сумма платежа'])*100,2)
        list_data.append(dic)
    return list_data
#print(common_information(df))

def greetings(str):
    '''возвращает привествие пользователю в зависимости от текущего времени суток'''
    date_obj = datetime.strptime(str,'%Y-%m-%d %H:%M:%S')
    if date_obj.hour in [0,10]:
        return "Доброе утро!"
    elif 10< date_obj.hour <= 16:
        return "Доброго дня!"
    elif 16< date_obj.hour <= 10:
        return "Доброго вечера!"
    elif 16< date_obj.hour <= 24:
        return "Доброй ночи!"

def get_exchange_rate(curr_list: list)->list:
    '''получает json-файл с кодировкой иностранных валют и url-ссылку по обменным курсам валют и
         возвращает значения текущих котировок этих валют'''
    total_list =[]
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    if response.status_code == 200:
        data_curr = response.json()
        for i in curr_list:
            dic = {}
            dic['currency'] = i
            dic['exchange_rate']=data_curr["Valute"][i]["Value"]
            total_list.append(dic)
    return total_list
# print(get_exchange_rate(d_fr=df))

def get_stock_price (json_file)->list:
    '''получает json-файл с наименованиями ценных бумаг и url-ссылку на котировки ценных бумаг и
     возвращает их текущие котировки'''
    total_list=[]
    url = "https://financialmodelingprep.com/api/v3/stock/list?apikey=e8auf9i7NE4i7YDiJBQqGdPhEaL8xj0K"
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    stock_list = json.loads(data)
    with open ((os.path.join('../data/',json_file)), 'r') as file:
        user_shares = json.load(file)
    for i in user_shares["user_stocks"]:
        for q in stock_list:
            if i==q["symbol"]:
                dic = {}
                dic['stock'] = i
                dic['price'] = q["price"]
                total_list.append(dic)
    return total_list
#print(get_stock_price(json_file='user_settings.json')

def main():
    agg_dict = {'greetings':greetings('2022-12-10 15:45:11'),
    'cards':common_information(json_data),
    'top_transactions':top_5_operations(json_data),
    'currency_rates':get_stock_price('user_settings.json'),
    'stock_prices':get_stock_price('user_settings.json')}
    return agg_dict
print(main())