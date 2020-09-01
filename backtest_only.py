# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:19:39 2020

@author: Harsh
"""

#import spe.bt_backtest as backtester
import spe as bt
import pandas as pd


def backtest(ticker_name,strat_name):
    # Enter Ticker Details
    ex = 'bo'
    market_type = 'equity'
    timeframe = 1440

    ticker = ticker_name if isinstance(ticker_name,str) else tuple(i for i in ticker_name)

    strategy = strat_name
    start_cash = 10000
    trade_size = 1
#    strat_object = backtester.main(ex, market_type, timeframe, ticker, strategy, trade_size, start_cash)
    df = pd.DataFrame()
    dff = bt.main(ex, market_type, timeframe, ticker, strategy, trade_size, start_cash,df)
    return dff

if __name__ == "__main__":
    
    # Enter Ticker Details
    ex = 'bo'
    market_type = 'equity'
    timeframe = 10080
    # ticker = ('ACC.BO',)
    # ticker = ('AJPH.BO',)
    # ticker = ('RLCP.BO',)
    # ticker = ('HDFC.BO','AJPH.BO','RLCP.BO')

    ticker = ('MICR.BO','63MO.BO')

    # Enter Strategy Name
    strategy = 'LTF3'
    
    # Enter Trade details
    start_cash = 10000
    trade_size = 1
#    strat_object = backtester.main(ex, market_type, timeframe, ticker, strategy, trade_size, start_cash)
    df = pd.DataFrame()
    dff = bt.main(ex, market_type, timeframe, ticker, strategy, trade_size, start_cash,df)
    
    dff.info()
    print(dff.head(500))
    dff.to_csv("/home/daksh/Main/Clearmind/Clearmind Dashboard/test.csv")
    
