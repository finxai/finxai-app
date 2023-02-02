import pandas as pd
from urllib.request import urlopen
import json
import time
import fxcmpy
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from sqlalchemy import create_engine
import bs4 as bs
import requests
from alpha_vantage.timeseries import TimeSeries

engine = create_engine('mysql+pymysql://root:xxx@localhost:3000', echo=False)  # root and port have been changed
db1 = engine.raw_connection()

# Connection to FXCM broker for getting the tickers for FOREX pairs
TOKEN = 'Insert FXCM TOKEN'
con = fxcmpy.fxcmpy(access_token=TOKEN, log_level='error')
instruments = con.get_instruments_for_candles()
con.close()

# Connection to Alpaca broker for getting the tickers for US stocks
ALPACA_API_KEY = "Insert ALPACA API Key"
ALPACA_API_SECRET = "Insert ALPACA API Secret Key"
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET)
search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
assets = trading_client.get_all_assets(search_params)
tickers_us = []
for i in assets:
    for k, v in dict(i).items():
        if k == "symbol":
            tickers_us.append(v)

# Connection to Alpaca broker for getting the tickers for cryptocurrencies
search_params2 = GetAssetsRequest(asset_class=AssetClass.CRYPTO)
assets_cryp = trading_client.get_all_assets(search_params2)
tickers_crypto = []
for i in assets_cryp:
    for k, v in dict(i).items():
        if k == "symbol":
            tickers_crypto.append(v)

# Extracting historical data for forex pairs
FMP_API_key = 'Insert FMP Token'
url = urlopen('https://financialmodelingprep.com/api/v3/symbol/available-forex-currency-pairs?apikey=' + FMP_API_key)
raw_data = json.load(url)
pairs_list = []
for i in raw_data:
    for k, v in i.items():
        if k == 'symbol':
            pairs_list.append(v)

alpha_API_key = 'Insert Alpha Vantage Token'
close_prices = pd.DataFrame()
forex_pairs = []
for i in instruments:
    pair = i.replace('/', '')
    forex_pairs.append(pair)
only_forex_list = []
for i in forex_pairs:
    if i in pairs_list:
        only_forex_list.append(i)

cp_tickers = only_forex_list  # forex_pairs
attempt = 0
drop = []
while len(cp_tickers) != 0 and attempt <= 10:
    print("-----------------")
    print("attempt number ", attempt)
    print("-----------------")
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)):
        try:
            ts = TimeSeries(key=alpha_API_key, output_format='pandas')
            data = ts.get_daily_adjusted(symbol=cp_tickers[i], outputsize='full')[0]
            data.columns = ["open", "high", "low", "close", "adjusted_close", "volume", "dividend", "split"]
            close_prices[cp_tickers[i]] = data["adjusted_close"]
            drop.append(cp_tickers[i])
        except:
            print(cp_tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1
    time.sleep(65)

forex_prices = close_prices.copy()
forex_prices.to_sql(con=engine, name='forex_prices', index=False, if_exists='append',
                                  schema='finxai_hist_price')

# Extracting the stock data from Alpaca
client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET)
start_date = pd.to_datetime("2013-01-01")
end_date = pd.to_datetime("2023-01-30")
html = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(html.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})
sp_tickers = []
for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        sp_tickers.append(ticker)

stock_prices = pd.DataFrame()
cp_tickers = sp_tickers
attempt = 0
drop = []
while len(cp_tickers) != 0 and attempt <= 5:
    print("-----------------")
    print("attempt number ", attempt)
    print("-----------------")
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)):
        try:
            request_params = StockBarsRequest(symbol_or_symbols=cp_tickers[i], timeframe=TimeFrame.Day,
                                   start=start_date, end=end_date)
            data = client.get_stock_bars(request_params).df
            data.columns = ["open", "high", "low", "close", "volume", "trade", "vwap"]
            data.reset_index(inplace=True)
            data.drop(["symbol"], axis=1, inplace=True)
            data.set_index(["timestamp"], inplace=True)
            stock_prices[cp_tickers[i]] = data["close"]
            drop.append(cp_tickers[i])
        except:
            print(cp_tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1

stock_prices.reset_index().to_sql(con=engine, name='stock_prices', index=False, if_exists='append',
                                  schema='finxai_hist_price')

# Extracting the crypto data from Alpaca
client = CryptoHistoricalDataClient()
start_date = pd.to_datetime("2018-12-30")
end_date = pd.to_datetime("2023-01-30")
crypto_prices = pd.DataFrame()
cp_tickers = tickers_crypto
attempt = 0
drop = []
while len(cp_tickers) != 0 and attempt <= 5:
    print("-----------------")
    print("attempt number ", attempt)
    print("-----------------")
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)):
        try:
            request_params = CryptoBarsRequest(symbol_or_symbols=cp_tickers[i], timeframe=TimeFrame.Day,
                                   start=start_date, end=end_date)
            data = client.get_crypto_bars(request_params).df
            data.columns = ["open", "high", "low", "close", "volume", "trade", "vwap"]
            data.reset_index(inplace=True)
            data.drop(["symbol"], axis=1, inplace=True)
            data.set_index(["timestamp"], inplace=True)
            crypto_prices[cp_tickers[i]] = data["close"]
            drop.append(cp_tickers[i])
        except:
            print(cp_tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1

crypto_prices.reset_index().to_sql(con=engine, name='crypto_prices', index=False, if_exists='append',
                                  schema='finxai_hist_price')

db1.close()
