import json
from src.views import get_excel

data_f= get_excel('operations.xlsx')
#df_=data[(data['datetime'].dt.year == 2020)&(data['datetime'].dt.month == 07)]

def most_profit_cashback (data,year,month):
    '''возвращает повышенные категории кэшбека из списка транзакций за определенные месяц и год'''
    final_list = []
    df = data[(data['datetime'].dt.year == year) & (data['datetime'].dt.month == month)]
    #print(df)
    data_gr = df.groupby(by='Категория').agg({'Кэшбэк': 'sum'})
    df_final = data_gr[data_gr['Кэшбэк'] != 0].sort_values(by='Кэшбэк', inplace=False, ascending=False).reset_index()
    #print (df_final.columns.values)
    for _, row in df_final.iterrows():
        dic = {}
        key = f'Категория {row['Категория']}'
        dic[key] = row['Кэшбэк']
        final_list.append(dic)
    return json.dumps(final_list,ensure_ascii=False)
print(most_profit_cashback(data_f,2020,8))