import pandas as pd
import numpy as np
import random
from scipy.optimize import minimize
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

engine = create_engine('mysql+pymysql://root:ehm3@localhost:3306', echo=False)
db1 = engine.raw_connection()

# Loading Pricing Data
querry_ins = "SELECT * FROM finxai_hist_price.instrument_universe"
instrument_universe = pd.read_sql(querry_ins, con=engine, index_col='date')


def get_riskadj_tickers(risk_profile):
    """
    Extracts the tickers related to each type of risk profile
    :param risk_profile: string
        Classification given to the investor by the Risk Classifier Algo or set by the user
    :return: list, list, list
        Returns lists with the tickers of the instruments being: stock tickers, forex tickers and crypto tickers
    """
    querrystck = "SELECT ticker FROM finxai_hist_price.stock_segment WHERE risk_profile =" + risk_profile
    stock = pd.read_sql(querrystck, con=engine)['ticker'].tolist()
    querryfx = "SELECT ticker FROM finxai_hist_price.forex_segment WHERE risk_profile =" + risk_profile
    forex = pd.read_sql(querryfx, con=engine)['ticker'].tolist()
    querrycrypto = "SELECT ticker FROM finxai_hist_price.crypto_segment WHERE risk_profile =" + risk_profile
    crypto = pd.read_sql(querrycrypto, con=engine)['ticker'].tolist()

    num_inst_per_port = 100

    try:
        if risk_profile == "'RN'":
            stock = random.sample(stock, int(num_inst_per_port * 0.6))
            forex = random.sample(forex, int(num_inst_per_port * 0.3))
            crypto = random.sample(crypto, int(num_inst_per_port * 0.1))
        elif risk_profile == "'RT'":
            stock = random.sample(stock, int(num_inst_per_port * 0.4))
            forex = random.sample(forex, int(num_inst_per_port * 0.3))
            crypto = random.sample(crypto, int(num_inst_per_port * 0.3))
        elif risk_profile == "'RA'":
            stock = random.sample(stock, int(num_inst_per_port * 0.6))
            forex = random.sample(forex, int(num_inst_per_port * 0.4))
            crypto = random.sample(forex, int(num_inst_per_port * 0))
    except:
        print("Probably we're requiring more tickers than those available to the risk profile")
    return stock + forex + crypto

def annualize_vol(r, periods_per_year):
    """
    Annualizes the vol of a set of returns
    We should infer the periods per year
    """
    return r.std() * (periods_per_year ** 0.5)

def annualize_rets(r, periods_per_year):
    """
    Annualizes a set of returns
    We should infer the periods per year
    """
    compounded_growth = (1 + r).prod()
    n_periods = r.shape[0]
    return compounded_growth ** (periods_per_year / n_periods) - 1

def sharpe_ratio(r, riskfree_rate, periods_per_year):
    """
    Computes the annualized sharpe ratio of a set of returns
    """
    # convert the annual riskfree rate to per period
    rf_per_period = (1 + riskfree_rate) ** (1 / periods_per_year) - 1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    ann_vol = annualize_vol(r, periods_per_year)
    return ann_ex_ret / ann_vol

def portfolio_return(weights, returns):
    """
    Computes the return on a portfolio from constituent returns and weights
    weights are a numpy array or 1 x N matrix and returns are a numpy array or NxN matrix
    """
    return weights.T @ returns

def portfolio_vol(weights, covmat):
    """
    Computes the volatility of a portfolio from a covariance matrix and constituent weights
    weights are a numpy array or N x 1 maxtrix and covmat is an N x N matrix
    """
    return (weights.T @ covmat @ weights) ** 0.5

def msr(riskfree_rate, er, cov):
    """
    Returns the weights of the portfolio that gives you the maximum sharpe ratio
    given the riskfree rate and expected returns (annual returns) and a covariance matrix
    """
    n = er.shape[0]
    init_guess = np.repeat(1 / n, n)
    bounds = ((0.0, 1.0),) * n  # an N-tuple of 2-tuples!
    # construct the constraints
    weights_sum_to_1 = {'type': 'eq',
                        'fun': lambda weights: np.sum(weights) - 1
                        }

    def neg_sharpe(weights, riskfree_rate, er, cov):
        """
        Returns the negative of the sharpe ratio
        of the given portfolio
        """
        r = portfolio_return(weights, er)
        vol = portfolio_vol(weights, cov)
        return -(r - riskfree_rate) / vol

    weights = minimize(neg_sharpe, init_guess,
                       args=(riskfree_rate, er, cov), method='SLSQP',
                       options={'disp': False},
                       constraints=(weights_sum_to_1,),
                       bounds=bounds)
    return weights.x

def gmv(cov, riskfree_rate):
    """
    Returns the weights of the Global Minimum Volatility portfolio
    given a covariance matrix
    """
    n = cov.shape[0]
    return msr(riskfree_rate, np.repeat(1, n), cov)

def capm_weights(returns, risk_free, periods_in_year):
    """Returns the weights of a Portfolio based on CAPM
    returns: Series or DataFrame with the returns of a number of stocks
    risk_free: Risk free rate
    periods_in_year: 12 for monthly data, 252 for daily"""
    risk_free_period = (1+risk_free) ** (1/periods_in_year) - 1
    Sinv = np.linalg.inv(returns.cov())
    Z = Sinv.dot(returns.mean() - risk_free_period)
    Z = pd.DataFrame(Z, index=returns.columns)
    return Z / np.sum(Z)

# Risk Free Rate
riskfree = 0.0353

tickers = get_riskadj_tickers(risk_profile="'RN'")
portfolio_user = instrument_universe[tickers]
portfolio_user_rts = np.log(portfolio_user.div(portfolio_user.shift(1))).dropna()

# Portfolio Correlation and Corr Matrix Graph
correl_port = portfolio_user_rts.corr()
_ = sns.heatmap(correl_port, cmap='jet')
_ = plt.title('Portfolio Correlation Matrix', fontsize=20)

# Performing analysis and allocating weights
port_ann_rts = annualize_rets(portfolio_user_rts.resample('M').last(), 12)
port_weights = capm_weights(portfolio_user_rts.resample('M').last(), riskfree, 12)
port_weights = pd.DataFrame(port_weights).T
port_weights.columns = portfolio_user_rts.columns
port_weights = port_weights.rename(index={0: 'Portfolio 0'})

# Generating the Portfolio Performance Graph
port_rts = portfolio_return(port_weights.T, portfolio_user_rts.T).T
wlth_idx = 1000 * (1 + port_rts).cumprod()
_ = wlth_idx.plot(grid=True)
_ = plt.xlabel('Period', fontsize=16)
_ = plt.ylabel('Wealth Index', fontsize=16)
_ = plt.title('Portfolio Performance', fontsize=20)
plt.show()

# Generating the Pie Chart of Portfolio Asset Allocation
df_transit = port_weights.T
df_transit = df_transit[df_transit.values > 0.009]
weig_vals = []
for i in df_transit.values:
    weig_vals.append(i[0])
weig_vals = np.array(weig_vals)
weig_labels = []
for i in df_transit.index:
    weig_labels.append(i)
weig_labels = np.array(weig_labels)

_ = plt.pie(weig_vals, autopct='%1.1f%%')
_ = plt.legend(weig_labels, loc='center right', bbox_to_anchor=(1.58, 0.5), fontsize=14)
_ = plt.title('Portfolio allocation at 3% risk free rate', fontsize=15)
cc = plt.Circle((0, 0), 0.75, color='black', fc='white', linewidth=1.25)
fig = plt.gcf()
_ = fig.gca().add_artist(cc)
plt.show()
