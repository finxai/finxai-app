import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dataprep.eda.missing import plot_missing
from sklearn.cluster import KMeans
sns.set()

engine = create_engine("mysql+pymysql://root:xxx@localhost:3xxx", echo=False)  # root and port have been changed
db1 = engine.raw_connection()

# Data preprocessing of Crypto Prices
querry_port = 'SELECT * FROM finxai_hist_price.crypto_prices'
crypto = pd.read_sql(querry_port, con=engine, index_col='timestamp')
plot_missing(crypto.copy()).show_browser()
filter = pd.DataFrame(crypto.isna().sum() / len(crypto) > 0.55)
rm_cols = filter[filter.iloc[:, 0] == True].index.tolist()
crypto.drop(rm_cols, axis=1, inplace=True)
crypto.fillna(method='bfill', inplace=True)
crypto_rtn = np.log(crypto.div(crypto.shift(1))).dropna()
summary = crypto_rtn.describe().T.loc[:, ["mean", "std"]]
summary["mean"] = summary["mean"] * 252
summary["std"] = summary["std"] * np.sqrt(252)
summary.plot.scatter(x="std", y="mean", s=50, fontsize=15)
for i in summary.index:
    plt.annotate(i, xy=(summary.loc[i, "std"] + 0.002, summary.loc[i, "mean"] + 0.002), size=9)
kmeans = KMeans(3)
kmeans.fit(summary)
summary["clusters"] = kmeans.fit_predict(summary)
_ = plt.scatter(summary["std"], summary["mean"], c=summary["clusters"], cmap="rainbow")
for i in summary.index:
    plt.annotate(i, xy=(summary.loc[i, "std"] + 0.002, summary.loc[i, "mean"] + 0.002), size=9)
plt.xlabel("Std", size=15)
plt.ylabel("Mean", size=15)
plt.legend(summary['clusters'], loc="upper left", fancybox=True)
summary["risk_profile"] = np.where(summary["std"] > 0.8, "RT", "RN")
summary.to_sql(con=engine, name='crypto_segment', index=False, if_exists='append',
                                  schema='finxai_hist_price')

# Data preprocessing of Stock Prices
querry_port = 'SELECT * FROM finxai_hist_price.stock_prices'
stock = pd.read_sql(querry_port, con=engine, index_col='timestamp')
filter = stock.isna().sum()/len(stock) > 0.05
rm_cols = filter.index[np.flatnonzero(filter)].tolist()
stock.drop(rm_cols, axis=1, inplace=True)
plot_missing(stock.copy()).show_browser()
stock.fillna(stock.mean(), inplace=True)
stock_rtn = np.log(stock.div(stock.shift(1))).dropna()
summary_stck = stock_rtn.describe().T.loc[:, ["mean", "std"]]
summary_stck["mean"] = summary_stck["mean"] * 252
summary_stck["std"] = summary_stck["std"] * np.sqrt(252)
summary_stck.plot.scatter(x="std", y="mean", s=50, fontsize=15)
for i in summary_stck.index:
    plt.annotate(i, xy=(summary_stck.loc[i, "std"] + 0.002, summary_stck.loc[i, "mean"] + 0.002), size=9)
kmeans = KMeans(4)
kmeans.fit(summary_stck)
summary_stck["clusters"] = kmeans.fit_predict(summary_stck)
_ = plt.scatter(summary_stck["std"], summary_stck["mean"], c=summary_stck["clusters"], cmap="rainbow")
for i in summary_stck.index:
    plt.annotate(i, xy=(summary_stck.loc[i, "std"] + 0.002, summary_stck.loc[i, "mean"] + 0.002), size=9)
plt.xlabel("Std", size=15)
plt.ylabel("Mean", size=15)
plt.legend(summary['clusters'], loc="upper left", fancybox=True)
summary_stck["risk_profile"] = np.where((summary_stck.clusters == 1) | (summary_stck.clusters == 2), "RT", np.nan)
summary_stck["risk_profile"] = np.where(summary_stck.clusters == 3, "RN", summary_stck.risk_profile)
summary_stck["risk_profile"] = np.where(summary_stck.clusters == 0, "RA", summary_stck.risk_profile)
summary_stck.to_sql(con=engine, name='stock_segment', index=False, if_exists='append',
                                  schema='finxai_hist_price')

# Data preprocessing of FOREX Parities
querry_port = 'SELECT * FROM finxai_hist_price.forex_prices'
forex = pd.read_sql(querry_port, con=engine, index_col='date')
plot_missing(forex.copy()).show_browser()
filter = forex.isna().sum()/len(forex) > 0.27
rm_cols = filter.index[np.flatnonzero(filter)].tolist()
forex.drop(rm_cols, axis=1, inplace=True)
forex.fillna(forex.mean(), inplace=True)
forex_rtn = np.log(forex.div(forex.shift(1))).dropna()
summary_fx = forex_rtn.describe().T.loc[:, ["mean", "std"]]
summary_fx["mean"] = summary_fx["mean"] * 252
summary_fx["std"] = summary_fx["std"] * np.sqrt(252)
summary_fx.plot.scatter(x="std", y="mean", s=50, fontsize=15)
for i in summary_fx.index:
    plt.annotate(i, xy=(summary_fx.loc[i, "std"] + 0.002, summary_fx.loc[i, "mean"] + 0.002), size=9)
kmeans = KMeans(3)
kmeans.fit(summary_fx)
summary_fx["clusters"] = kmeans.fit_predict(summary_fx)
_ = plt.scatter(summary_fx["std"], summary_fx["mean"], c=summary_fx["clusters"], cmap="rainbow")
for i in summary_fx.index:
    plt.annotate(i, xy=(summary_fx.loc[i, "std"] + 0.002, summary_fx.loc[i, "mean"] + 0.002), size=9)
plt.xlabel("Std", size=15)
plt.ylabel("Mean", size=15)
plt.legend(ncols=3)
summary_fx["risk_profile"] = np.where(summary_fx.clusters == 1, "RT", np.nan)
summary_fx["risk_profile"] = np.where(summary_fx.clusters == 2, "RN", summary_fx.risk_profile)
summary_fx["risk_profile"] = np.where(summary_fx.clusters == 0, "RA", summary_fx.risk_profile)
summary_fx.to_sql(con=engine, name='forex_segment', index=False, if_exists='append',
                                  schema='finxai_hist_price')

db1.close()
