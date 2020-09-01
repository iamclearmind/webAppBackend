# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 18:33:13 2020

@author: Harsh
"""

import timeit
import importlib
import datetime
import backtrader as bt
import pandas as pd
import logging
#import pyfolio as pf

import spe.screenerUtil as su
import spe.data_handler_backtest as dh
     
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo

def bt_run(strat_p_list,df):
    
    # Create a cerebro entity
    try:
        
        cerebro = bt.Cerebro(tradehistory=True)
        cerebro.addanalyzer(bt.analyzers.cmtrans.cmTrans)
        # cerebro.addwriter(bt.WriterFile, out = 'test.csv', csv=True, rounding=5)
        
        data_table_id = strat_p_list[0]
        scrip_code = strat_p_list[1]
        strategy = strat_p_list[2]
        trade_size = strat_p_list[3]
        start_cash = strat_p_list[4]
        
        ex,m_t,t_f = su.parameters_from_data_table_id(data_table_id)
        
        # Get Class from strategy Name
        module = importlib.import_module('spe.strategies.'+strategy)
        class_name = strategy
        strategy = getattr(module, class_name)
        
        # Add a strategy
        cerebro.addstrategy(strategy,trade_size=trade_size)
        
        # Minimum datalength
        min_data = strategy.candle_lb()
        
        # Add the Data Feed to Cerebro
        # Returns Cerebro riteith datafeed attached
        cerebro_w_data = dh.data_feed(scrip_code,ex,m_t,t_f,cerebro,min_data)
        
        if cerebro_w_data is None:
            print('No Data Available')
            return []
        
        # Set our desired cash start
        cerebro_w_data.broker.setcash(start_cash)     
    
        # Set the commission - 0.1% ... divide by 100 to remove the %
        cerebro_w_data.broker.setcommission(commission=0.000)
        
        # cerebro_w_data.addanalyzer(bt.analyzers.TradeAnalyzer, _name="stats")
        # cerebro_w_data.addanalyzer(bt.analyzers.PositionsValue, _name="an_return")
        cerebro_w_data.addanalyzer(bt.analyzers.Returns)
        # cerebro_w_data.addanalyzer(bt.analyzers.PyFolio)
        
        # Print out the starting conditions
#        print('Starting Portfolio Value: %.2f' % cerebro_w_data.broker.getvalue())
    
        # Run over everything
        strategy = cerebro_w_data.run()
        b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
        # cerebro_w_data.plot(b)
        Strat = strategy[0]
        # Print out the final result
#        print('Final Portfolio Value: %.2f' % cerebro_w_data.broker.getvalue())
    
        # Strat.analyzers.stats.print()
        # Strat.analyzers.an_return.print()
#        print(f"Norm. Annual Return: {Strat.analyzers.returns.get_analysis()['rnorm100']:.2f}%")
        # pyfolizer = Strat.analyzers.getbyname('pyfolio')
        # returns, positions, transactions, gross_lev = pyfolizer.get_pf_items()
        # pf.create_returns_tear_sheet(returns)
        
        df = backtest_out(Strat,df)
        
        return Strat,df

    except Exception as e:
        # err.error_log(str(e),bt_run.__name__,'bt_run')
        logging.exception(str(e))
    
 
def main(ex,mt,tf,ticker,strat_name,t_s,start_cash,df):
    
    try:
        
        start = timeit.default_timer()

        datasource = 'ohlcv_{e}_{m}_{t}'.format(e=ex.lower(),m=mt.lower(),t=tf)
        
        strategy_parameters = (datasource, ticker, strat_name, t_s, start_cash )
                               # None, 'output_csv/', 'cmOne_bo')
        
        Strat,df = bt_run(strategy_parameters,df)
        # print(data_value_json)
        # execution_time logger
        stop = timeit.default_timer()
        execution_time = stop - start
        print("Program Executed in "+str(execution_time) )
        return df

    except Exception as e:
        # err.error_log(str(e),main.__name__,'bt_run')
        logging.exception(str(e))
  
def backtest_out(strat_object,df):
    
    ls = strat_object.analyzers.cmtrans._pos
    
    if not ls:
        return
    
    df = pd.DataFrame(ls,columns=['Type','Date','Ticker','Position','Price','PnL','ROE','Trade_Length'])
#    df.set_index('Date',inplace=True)
#    df = df[[['Type','Date','Ticker','Position','Price','PnL','ROE','Trade_Length']]]
    df['Cumm'] = df['PnL'].cumsum()
    Roll_Max = df['Cumm'].cummax()
    Daily_Drawdown = Roll_Max - df['Cumm']
    df['DD'] = Daily_Drawdown

    return df
       
if __name__ == "__main__":
    
    # Enter Ticker Details
    ex = 'ns'
    market_type = 'equity'
    timeframe = 10080
    ticker = ('HDFC.NS', 'TAMO.NS', 'HLL.NS')

    # Enter Strategy Name
    strategy = 'rsiStrat_multi'
    
    # Enter Trade details
    start_cash = 10000
    trade_size = 1
    strat_object = main(ex,market_type,timeframe,ticker,strategy,trade_size,start_cash)

    

    






