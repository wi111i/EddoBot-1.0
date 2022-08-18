import pandas as pd
import numpy as np
import math
import requests
import xlsxwriter
from secrets_API import IEX_CLOUD_API_TOKEN

stocks = pd.read_csv('sp_500_stocks.csv')

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
stock_price = data['latestPrice']
mkt_cap = data['marketCap']
my_columns = ['Ticker', 'Stock Price ($USD)', 'Market Cap ($B)', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)
final_dataframe = final_dataframe.append(
    pd.Series(
    [
        symbol, 
        stock_price, 
        mkt_cap, 
        'N/A'
    ], 
    index = my_columns
    ),
    ignore_index = True
)

final_dataframe = pd.DataFrame(columns = my_columns)
for stock in stocks['Ticker'][:5]:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
    final_dataframe = final_dataframe.append(
        pd.Series([
            stock, 
            data['latestPrice'],
            data['marketCap']/1000000000, 
            'N/A'], 
            index = my_columns), 
        ignore_index = True
    )
print(final_dataframe)