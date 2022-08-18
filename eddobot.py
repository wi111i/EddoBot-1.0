import pandas as pd
import numpy as np
import math
import requests
import xlsxwriter
from secrets_API import IEX_CLOUD_API_TOKEN

stocks = pd.read_csv('sp_500_stocks.csv')
stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC','VIAC','WLTW'])]

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
stock_data = requests.get(api_url).json()
stock_price = stock_data['latestPrice']
mkt_cap = stock_data['marketCap']
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
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []

for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

final_dataframe = pd.DataFrame(columns = my_columns)
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
                [
                symbol, 
                data[symbol]['quote']['latestPrice'], 
                data[symbol]['quote']['marketCap'], 
                'N/A'
                ], 
                index = my_columns), 
                ignore_index = True
            )

portfolio_size = input("Enter the value of your portfolio:")

try:
    val = float(portfolio_size)
except ValueError:
    print("That's not a number! \n Try again:")
    portfolio_size = input("Enter the value of your portfolio:")
position_size = float(portfolio_size) / len(final_dataframe.index)
for i in range(0, len(final_dataframe['Ticker'])-1):
    final_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size / final_dataframe['Price'][i])

print(final_dataframe)