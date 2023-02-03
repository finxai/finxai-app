import pandas as pd
import fxcmpy
import numpy as np
import seaborn as sns
import time
from datetime import datetime
import pickle
sns.set()
rl_model = pickle.load(open("EURUSD_bin_class", "rb"))
col = ["tradeId", "amountK", "currency", "grossPL", "isBuy"]

class DNNTrader:
    def __init__(self, instrument, bar_length, window, lags, model, units):
        self.ticker = instrument
        self.bar_length = pd.to_timedelta(bar_length)
        self.tick_data = None
        self.raw_data = None
        self.data = None
        self.ticks = 0  # running tick number
        self.last_bar = None
        self.units = units
        self.position = 0

        # ********************************* add strategy-specific attributes here *********************************
        self.window = window
        self.lags = lags
        self.model = model
        # *********************************************************************************************************

    def get_most_recent(self, period="m1", number=10000):
        """
        Gets the historical mid-price of an instrument
        PARAMETERS
        ----------
        :param period: str
            Periodicity of the candles to use
        :param number: int
            The number of past candles to call
        :return: None
        """
        while True:
            time.sleep(5)
            df = api.get_candles(self.ticker, number=number, period=period, columns=["bidclose", "askclose"])
            df[self.ticker] = (df.bidclose + df.askclose) / 2
            df = df.resample(self.bar_length, label="right").last().dropna().iloc[:-1]
            self.raw_data = df.copy()
            self.last_bar = self.raw_data.index[-1]
            if pd.to_datetime(datetime.utcnow()) - self.last_bar < self.bar_length:
                self.start_time = pd.to_datetime(datetime.utcnow())
                break

    def get_tick_data(self, data, df):
        """
        Requires that we subscribe to an instrument using FXCM API, it's passed as a parameter
        Collects and stores the tick data of a subscribed instrument using the mid-price and sending to execute
        the strategy.
        It also determines the stop of the trading session
        PARAMETERS
        ------------
        :param data: float
            price information from the instrument, Ask and Bid
        :param df: DataFrame
            Df which stores the price information
        :return: None
        """
        self.ticks += 1
        print(self.ticks, end=" ")  # Print running tick number

        recent_tick = pd.to_datetime(data["Updated"], unit="ms")

        # define a trading stop
        if recent_tick.time() >= pd.to_datetime("15:00").time():
            api.unsubscribe_market_data(self.ticker)
            if len(api.get_open_positions()) != 0:
                api.close_all_for_symbol(self.ticker)
                print(2 * "\n" + "{} | GOING NEUTRAL".format(str(datetime.utcnow())) + "\n")
                time.sleep(20)
                print(api.get_closed_positions_summary()[col])
            self.position = 0
            api.close()

        # Collect and store tick data (mid-price only)
        # If a time longer than the bar length has elapsed between the last full bar and the most recent tick
        if recent_tick - self.last_bar > self.bar_length:
            # Get most recent ticks since last full bar
            self.tick_data = df.loc[self.last_bar:, ["Bid", "Ask"]]
            self.tick_data[self.ticker] = (self.tick_data.Ask + self.tick_data.Bid) / 2
            self.tick_data = self.tick_data[self.ticker].to_frame()
            self.resample_and_join()
            self.define_strategy()
            self.execute_trades()

    def resample_and_join(self):
        """
        Unites the historical price data collected from an instrument with the new tick data obtained by the stream
        :return: None
        """
        # Append the most recent ticks (resampled) to self.data
        self.raw_data = pd.concat([self.raw_data,
                                   self.tick_data.resample(self.bar_length, label="right").last().ffill().iloc[:-1]],
                                  axis=0)
        # We use "right" to use close prices
        # We don't forward fill with historical data because there could have been no data because of weekends or so
        self.last_bar = self.raw_data.index[-1]  # update time of the last full bar

    # strategy specific
    def define_strategy(self):
        data = self.raw_data.copy()

        # ======================= define the strategy here =======================
        # create features
        data = pd.concat([data, self.tick_data], axis=1)  # append latest tick (== open price of current bar)
        data["returns"] = np.log(data[self.ticker] / data[self.ticker].shift())
        data["dir"] = np.where(data["returns"] > 0, 1, 0)
        data["sma"] = data[self.ticker].rolling(self.window).mean() - data[self.ticker].rolling(150).mean()
        # noinspection PyUnresolvedReferences
        data["boll"] = (data[self.ticker] - data[self.ticker].rolling(self.window).mean())\
                       / data[self.ticker].rolling(self.window).std()
        data["min"] = data[self.ticker].rolling(self.window).min() / data[self.ticker] - 1
        data["max"] = data[self.ticker].rolling(self.window).max() / data[self.ticker] - 1
        data["mom"] = data["returns"].rolling(3).mean()
        data["vol"] = data["returns"].rolling(self.window).std()
        data.dropna(inplace=True)

        # create lags
        self.cols = []
        features = ["returns", 'dir', 'sma', 'boll', 'min', 'max', 'mom', 'vol']
        for f in features:
            for lag in range(1, self.lags + 1):
                col = "{}_lag_{}".format(f, lag)
                data[col] = data[f].shift(lag)
                self.cols.append(col)
        data.dropna(inplace=True)

        # scaling the data
        scaler = pickle.load(open("scaler_EURUSD", "rb"))
        data_s = scaler.transform(data[~data[[self.ticker, "dir"]]])
        # predict
        data["proba"] = self.model.predict(data_s)

        # determine positions
        data = data.loc[self.start_time:].copy()  # starting with first live_stream bar (removing historical bars)
        data["position"] = np.where(data.proba < 0.5, -1, np.nan)
        data["position"] = np.where(data.proba > 0.5, 1, data.position)
        data["position"] = data.position.ffill().fillna(0)  # start with neutral posiiton if no strong signal received
        # ===========================================================================

        self.data = data.copy()

    def execute_trades(self):
        """
        This execution code assumes that the trader account is a NETTING ACCOUNT not a HEDGING account
        Makes decisions regarding the position taken for a given instrument based on the defined strategy
        :return: None
        """
        if self.data["position"].iloc[-1] == 1:  # if position is long -> go/stay long
            if self.position == 0:
                order = api.create_market_buy_order(self.ticker, self.units)
                self.report_trade(order, "GOING LONG ON{}".format(self.ticker))
            elif self.position == -1:
                order = api.create_market_buy_order(self.ticker, self.units * 2)
                self.report_trade(order, "GOING LONG ON{}".format(self.ticker))
            self.position = 1
        elif self.data["position"].iloc[-1] == -1:  # if position is short -> go/stay short
            if self.position == 0:
                order = api.create_market_sell_order(self.ticker, self.units)
                self.report_trade(order, "GOING SHORT ON{}".format(self.ticker))
            elif self.position == 1:
                order = api.create_market_sell_order(self.ticker, self.units * 2)
                self.report_trade(order, "GOING SHORT ON{}".format(self.ticker))
            self.position = -1
        elif self.data["position"].iloc[-1] == 0:
            if self.position == -1:
                order = api.create_market_buy_order(self.ticker, self.units)
                self.report_trade(order, "GOING NEUTRAL ON{}".format(self.ticker))
            elif self.position == 1:
                order = api.create_market_sell_order(self.ticker, self.units)
                self.report_trade(order, "GOING NEUTRAL ON{}".format(self.ticker))
            self.position = 0

    def report_trade(self, order, going):
        """
        Provides information regarding newly taken positions during the trading session
        PARAMETERS
        ------------
        :param order: object
            fxcm object making the market order
        :param going: str
            text telling the position to be taken on a specific instrument
        :return: None
        """
        time_s = order.get_time()
        units = api.get_open_positions().amountK.iloc[-1]
        price = api.get_open_positions().open.iloc[-1]
        unreal_pl = api.get_open_positions().grossPL.sum()
        print("\n" + 100 * "-")
        print("{} | {}".format(time_s, going))
        print("{} | units = {} | price = {} | Unreal P&L = {}".format(time_s, units, price, unreal_pl))
        print(100 * "-" + "\n")

if __name__ == "__main__":
    TOKEN = 'FXCM_Token'
    attempt = 0
    raw = []
    while attempt <= 5 and len(raw) == 0:
        print("-----------------")
        print("Attempt Number: ", attempt)
        print("-----------------")
        time.sleep(3)
        try:
            api = fxcmpy.fxcmpy(access_token=TOKEN, log_level='error')
        except Exception as e:
            print("========Failed  to connect with FXCM API retrying========")
            print(e)
        else:  # only if no error occurred
            trader = DNNTrader("EUR/USD", bar_length="30min", window=50, lags=5, model=rl_model, units=100)
            trader.get_most_recent()
            api.subscribe_market_data(trader.ticker, (trader.get_tick_data,))
            raw.append([3, 3])
        finally:
            attempt += 1

