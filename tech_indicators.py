import datetime as dt  		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
from util import get_data, plot_data, symbol_to_path
import matplotlib.pyplot as plt


### calculate typical technical indicators for stocks #############

def EMA(prices, lookback):
    ema = prices.ewm(span = lookback, adjust = False).mean()
    return ema

def BBP(prices, lookback):
    rolling_std = prices.rolling(window=lookback, min_periods =lookback).std()
    sma = prices.rolling(window = lookback, min_periods = lookback).mean()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bbp = (prices - bottom_band) / (top_band - bottom_band)
    return bbp, top_band, bottom_band

def MOMENTUM(prices, lookback):
    momentum = prices/prices.shift(lookback) - 1
    return momentum

def RSI(prices, lookback):
    daily_return = prices/prices.shift(1) - 1
    up_rets = daily_return.copy().where(daily_return>=0, 0).cumsum()
    down_rets = daily_return.copy().where(daily_return<0, 0).cumsum() * (-1)
    up_gain = daily_return.copy()
    up_gain[:] = 0
    up_gain.values[lookback:] = up_rets.values[lookback:] - up_rets.values[: -lookback]
    down_loss = daily_return.copy()
    down_loss[:] = 0
    down_loss.values[lookback:] = down_rets.values[lookback:] - down_rets.values[: -lookback]
    rs = (up_gain / lookback) / (down_loss / lookback)
    rsi = 100 - (100 /(1+rs))
    rsi.iloc[:lookback] = np.nan
    rsi[rsi == np.inf] = 100
    return rsi

def MACD(prices):
    macd = EMA(prices, 12) - EMA(prices, 26)
    signal = macd.ewm(span = 9, adjust = False).mean()
    return macd, signal



def generate_plot():
    symbol = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices = prices_all[symbol]
    lookback = 14
    x_data = prices.index
    prices_norm = prices.copy()
    prices_norm = prices_norm/prices.iloc[0]

    # price/EMA
    plt.figure(1)
    ema = EMA(prices, lookback)
    ema_norm = ema.copy()
    ema_norm = ema_norm /ema.iloc[0]
    price_ema = prices_norm/ema_norm
    plt.plot(x_data, prices_norm, label="Price", color ="tab:blue")
    plt.plot(x_data, ema_norm, label="EMA", color ="orange")
    plt.plot(x_data, price_ema, label="Price/EMA", color ="tab:purple")
    plt.title("Indicator 1: Price/EMA")
    plt.xlabel("Date")
    plt.ylabel("Normalized Values")
    plt.legend(fontsize='10')
    #plt.show()
    plt.savefig('Figure-1.png')
    
    # BBP
    plt.figure(2)
    sma = prices.rolling(window = lookback, min_periods = lookback).mean()
    bbp, top_band, bottom_band = BBP(prices, lookback)
    plt.subplot(2,1,1)
    plt.plot(x_data, prices, label="Price", color ="tab:blue")
    plt.plot(x_data, sma, label="SMA", color ="orange")
    plt.plot(x_data, top_band, label="Top Band", color ="tab:red")
    plt.plot(x_data, bottom_band, label="Bottom Band", color ="tab:green")
    plt.title("Indicator 2: Bollinger Bands")
    plt.legend(fontsize='10')
    plt.ylabel("Actual Values")

    plt.subplot(2,1,2)
    plt.ylabel("% Values")
    plt.plot(x_data, bbp, label="Bollinger Band Percentage", color ="tab:purple")
    plt.xlabel("Date")
    plt.legend(fontsize='10')
    #plt.show()
    plt.savefig('Figure-2.png')

    # Momentum
    plt.figure(3)
    momentum = MOMENTUM(prices, lookback)
    plt.subplot(2,1,1)
    plt.plot(x_data, prices, label="Price", color ="tab:blue")
    plt.title("Indicator 3: Price Momentum")
    plt.legend(fontsize='10')
    plt.ylabel("Actual Values")

    plt.subplot(2,1,2)
    plt.ylabel("% Values")
    plt.plot(x_data, momentum, label="Price Momentum", color ="tab:purple")
    plt.xlabel("Date")
    plt.legend(fontsize='10')
    #plt.show()
    plt.savefig('Figure-3.png')

    # RSI
    plt.figure(4)
    rsi = RSI(prices, lookback)
    plt.subplot(2,1,1)
    plt.plot(x_data, prices, label="Price", color ="tab:blue")
    plt.title("Indicator 4: RSI")
    plt.legend(fontsize='10')
    plt.ylabel("Actual Values")

    plt.subplot(2,1,2)
    plt.plot(x_data, rsi, label="RSI", color ="tab:purple")
    plt.xlabel("Date")
    plt.ylabel("RSI Values")
    plt.legend(fontsize='10')
    #plt.show()
    plt.savefig('Figure-4.png')

    # MACD
    plt.figure(5)
    macd, signal = MACD(prices)
    plt.plot(x_data, macd, label="MACD", color ="tab:orange")
    plt.plot(x_data, signal, label="Signal", color ="tab:green")
    plt.title("Indicator 5: MACD")
    plt.xlabel("Date")
    plt.ylabel("Normalized Values")
    plt.legend(fontsize='10')
    #plt.show()
    plt.savefig('Figure-5.png')

if __name__ == "__main__":
    generate_plot()