import random
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
import bs4 as bs
import requests
from sqlalchemy import create_engine
from dataprep.eda.missing import plot_missing
import seaborn as sns
from sklearn.cluster import KMeans
sns.set()

ALPACA_API_KEY = "ALPACA_KEY"
ALPACA_API_SECRET = "ALPACA_SECRET"
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET)
search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
assets = trading_client.get_all_assets(search_params)
tickers_us = []
for i in assets:
    for k, v in dict(i).items():
        if k == "symbol":
            tickers_us.append(v)

html = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(html.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})
sp_tickers = []
for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        sp_tickers.append(ticker)

extra_tickers = random.sample(tickers_us, 500)
chosen_tickers = []
for i in extra_tickers:
    if i not in sp_tickers:
        chosen_tickers.append(i)

tickers_state = sp_tickers + chosen_tickers

# ===========================================================
engine = create_engine('mysql+pymysql://root:xxx@localhost:3000', echo=False)  # root and port have been changed
db1 = engine.raw_connection()
querry_acc_lst = "SELECT * FROM finxai_hist_price.account_names"
acc_lst = pd.read_sql(querry_acc_lst, con=engine)
acc_lst = acc_lst.tolist()

finan_statements = pd.DataFrame()
cp_tickers = tickers_state
attempt = 0
drop = []
while len(cp_tickers) != 0 and attempt <= 1:
    print("-----------------")
    print("attempt number ", attempt)
    print("-----------------")
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)):
        try:
            url = urlopen('http://api.finxai.com/financial-statements?ticker=' + cp_tickers[i])
            raw_data = json.load(url)
            # ======================================================
            for k, v in raw_data.items():
                if k == "ticker":
                    ticker = v

            for k, v in raw_data.items():
                if k == "income_statements":
                    inc_statement = pd.DataFrame()
                    for acc in range(len(v)):
                        df = pd.DataFrame(v[acc], index=[ticker])
                        inc_statement = pd.concat([inc_statement, df], axis=0)
                elif k == "balance_sheets":
                    bal_statement = pd.DataFrame()
                    for acc in range(len(v)):
                        df = pd.DataFrame(v[acc], index=[ticker])
                        bal_statement = pd.concat([bal_statement, df], axis=0)
                elif k == "cash_flows":
                    cash_statement = pd.DataFrame()
                    for acc in range(len(v)):
                        df = pd.DataFrame(v[acc], index=[ticker])
                        cash_statement = pd.concat([cash_statement, df], axis=0)

            dataf = pd.concat([inc_statement, bal_statement, cash_statement], axis=1)
            dataf = dataf.T.drop_duplicates().T
            supp_df = pd.DataFrame()
            for acc in acc_lst:
                try:
                    supp_df[acc] = dataf[acc]
                except:
                    print("Some accounts are missing")
            finan_statements = pd.concat([finan_statements, supp_df], axis=0)
            # ======================================================
            drop.append(cp_tickers[i])
        except:
            print(cp_tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1

dataset1 = finan_statements.reset_index()
dataset1.rename({"index": 'ticker'}, axis=1, inplace=True)
dataset1_num = dataset1.iloc[:, 2:].apply(pd.to_numeric)
dataset1_date = pd.to_datetime(dataset1['date'])
dataset_net = pd.concat([dataset1['ticker'], dataset1_date, dataset1_num], axis=1)
dataset_net.set_index('date', inplace=True)
plot_missing(dataset_net.reset_index().copy()).show_browser()

dataset_risk = dataset_net.loc['2021', :].reset_index().drop('date', axis=1).set_index('ticker')
filter = pd.DataFrame(dataset_risk.isna().sum() / len(dataset_risk) > 0.5)
rm_cols = filter[filter.iloc[:, 0] == True].index.tolist()
dataset_risk.drop(rm_cols, axis=1, inplace=True)
dataset_risk = dataset_risk.replace(0, np.nan)
dataset_risk.fillna(dataset_risk.mean(), inplace=True)

# Creating risk parameter columns
dataset_risk['return_gp_sales'] = dataset_risk.gross_profit.div(dataset_risk.sales)
dataset_risk['solvency1'] = dataset_risk.total_liabilities.div(dataset_risk.total_assets)

dataset_class = dataset_risk[["return_gp_sales", "solvency1"]]
dataset_class.plot.scatter(x="solvency1", y="return_gp_sales", s=50, fontsize=15)
for i in dataset_class.index:
    plt.annotate(i, xy=(dataset_class.loc[i, "std"] + 0.002, dataset_class.loc[i, "mean"] + 0.002), size=9)
kmeans = KMeans(3)
kmeans.fit(dataset_class)
dataset_class["clusters"] = kmeans.fit_predict(dataset_class)
_ = plt.scatter(dataset_class["solvency1"], dataset_class["return_gp_sales"],
                c=dataset_class["clusters"], cmap="rainbow", alpha=0.5)
for i in dataset_class.index:
    plt.annotate(i, xy=(dataset_class.loc[i, "solvency1"] + 0.002, dataset_class.loc[i, "return_gp_sales"] + 0.002), size=9)
plt.xlabel("solvency1", size=15)
plt.ylabel("return_gp_sales", size=15)
plt.legend(dataset_class['clusters'], loc="upper left", fancybox=True)

dataset_class['risk_profile'] = np.where(dataset_class['clusters'] == 1, 'RT', np.nan)
dataset_class['risk_profile'] = np.where(dataset_class['clusters'] == 0, "RA", dataset_class['risk_profile'])
dataset_class['risk_profile'] = np.where(dataset_class['clusters'] == 2, "RN", dataset_class['risk_profile'])

dataset_risk_fin = pd.concat([dataset_risk, dataset_class['risk_profile']], axis=1)
dataset_risk_fin.reset_index().to_sql(con=engine, name='fin_state_2021', index=False, if_exists='append',
                           schema='finxai_hist_price')

risk_class = dataset_risk_fin['risk_profile'].to_dict()
dataset_net["risk_profile"] = dataset_net['ticker'].map(risk_class)
dataset_net.reset_index().to_sql(con=engine, name='finan_statements', index=False, if_exists='replace',
                           schema='finxai_hist_price')

# Final data preprocessing
data_prepro =dataset_net.reset_index()
data_prepro = data_prepro[data_prepro['date'].notna()]
data_prepro = data_prepro[data_prepro['risk_profile'].notna()]
plot_missing(data_prepro.reset_index().copy()).show_browser()
data_prepro.set_index('date', inplace=True)
filter = pd.DataFrame(data_prepro.isna().sum() / len(data_prepro) > 0.4)
rm_cols = filter[filter.iloc[:, 0] == True].index.tolist()
data_prepro.drop(rm_cols, axis=1, inplace=True)
data_prepro = data_prepro.replace(0, np.nan)
data_prepro.fillna(data_prepro.mean(), inplace=True)

# Feature Engineering
data_y = data_prepro[['risk_profile']]
data_x = data_prepro.iloc[:, :-1]
cols_feat = []
for i in data_x.iloc[:, 2:]:
    col = "{}_sales".format(i)
    data_x[col] = data_x[i].div(data_x.sales)
    cols_feat.append(col)
data_x['solvency1'] = data_x.total_liabilities.div(data_x.common_shares)
data_x['solvency2'] = data_x.total_liabilities.div(data_x.total_assets)

data_financ_stat = pd.concat([data_y.reset_index(), data_x], axis=1)
data_financ_stat.to_sql(con=engine, name='finan_statements', index=False, if_exists='replace',
                           schema='finxai_hist_price')

db1.close()
