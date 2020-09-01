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

def bt_run(strat_p_list):
    
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
        print('Starting Portfolio Value: %.2f' % cerebro_w_data.broker.getvalue())
    
        # Run over everything
        strategy = cerebro_w_data.run()
        b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
        # cerebro_w_data.plot(b)
        Strat = strategy[0]
        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro_w_data.broker.getvalue())
    
        # Strat.analyzers.stats.print()
        # Strat.analyzers.an_return.print()
        print(f"Norm. Annual Return: {Strat.analyzers.returns.get_analysis()['rnorm100']:.2f}%")
        # pyfolizer = Strat.analyzers.getbyname('pyfolio')
        # returns, positions, transactions, gross_lev = pyfolizer.get_pf_items()
        # pf.create_returns_tear_sheet(returns)
        
        backtest_out(Strat)
        
        return Strat

    except Exception as e:
        # err.error_log(str(e),bt_run.__name__,'bt_run')
        logging.exception(str(e))
    
 
def main(ex,mt,tf,ticker,strat_name,t_s,start_cash):
    
    try:
        
        start = timeit.default_timer()

        datasource = 'ohlcv_{e}_{m}_{t}'.format(e=ex.lower(),m=mt.lower(),t=tf)
        
        strategy_parameters = (datasource, ticker, strat_name, t_s, start_cash )
                               # None, 'output_csv/', 'cmOne_bo')
        
        strat_object = bt_run(strategy_parameters)
        # print(data_value_json)
        
        # execution_time logger
        stop = timeit.default_timer()
        execution_time = stop - start
        print("Program Executed in "+str(execution_time) )
        return strat_object

    except Exception as e:
        # err.error_log(str(e),main.__name__,'bt_run')
        logging.exception(str(e))
  
def backtest_out(strat_object):
    
    ls = strat_object.analyzers.cmtrans._pos
    
    if not ls:
        return
    
    df = pd.DataFrame(ls,columns=['Type','Date','Ticker','Position','Price','PnL','ROE','Trade_Length'])
    df.set_index('Date',inplace=True)
    df['Cumm'] = df['PnL'].cumsum()
    Roll_Max = df['Cumm'].cummax()
    Daily_Drawdown = Roll_Max - df['Cumm']
    df['DD'] = Daily_Drawdown

    totalbars = strat_object.bar_counter
    intime = df['Trade_Length'].sum()


    df_len = len(df) + 1
    
    npnl = df['PnL'].sum()
    ttrades = df['PnL'].count()
    if ttrades != 0:
        avg_tret = round(df['ROE'].sum()/ttrades,2)
    else:
        avg_tret = 0
    Max_Daily_Drawdown = Daily_Drawdown.max()
    
    from os.path import expanduser
    home = expanduser("~")
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(home+'/output_data/backtest_out.xlsx', engine='xlsxwriter',
                            options={'nan_inf_to_errors': True})
    df.to_excel(writer, sheet_name='Sheet1')
    
    # Get the xlsxwriter objects from the dataframe writer object.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    
    # Create a chart object.
    chart = workbook.add_chart({'type': 'line'})
    
    # Configure the series of the chart from the dataframe data.
    chart.add_series({'categories': 'Sheet1!$A$2:$A${len}'.format(len=df_len),
                      'values': '=Sheet1!$I$2:$I${len}'.format(len=df_len)
                      })
    chart.show_blanks_as('span')
    # Insert the chart into the worksheet.
    worksheet.insert_chart('O2', chart)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    
    worksheet.write('L2', 'PnL', bold)
    worksheet.write('L3', 'Average Trade Return', bold)
    worksheet.write('L4', 'Trades', bold)
    worksheet.write('L5', 'Max DD', bold)
    worksheet.write('L6', 'In For Bars', bold)
    worksheet.write('L7', 'Total Bars', bold)

    worksheet.write('M2', npnl)
    worksheet.write('M3', avg_tret)
    worksheet.write('M4', ttrades)
    worksheet.write('M5', Max_Daily_Drawdown)
    worksheet.write('M6', intime)
    worksheet.write('M7', totalbars)

    multi_sheet_trade_formatter(df,writer,workbook,bold)
    
    workbook.close()
    
def multi_sheet_trade_formatter(df,writer,workbook,bold):
    
    grouped_ticker_obj = df.groupby('Ticker')
    
    for ticker, ticker_df in grouped_ticker_obj:

        df_len = len(ticker_df) + 1
        
        ticker_df['Cumm'] = ticker_df['PnL'].cumsum()
        Roll_Max = ticker_df['Cumm'].cummax()
        Daily_Drawdown = Roll_Max - ticker_df['Cumm']
        ticker_df['DD'] = Daily_Drawdown
    
        npnl = ticker_df['PnL'].sum()
        ttrades = ticker_df['PnL'].count()
        if ttrades != 0:
            avg_tret = round(df['ROE'].sum() / ttrades, 2)
        else:
            avg_tret = 0
        Max_Daily_Drawdown = Daily_Drawdown.max()

        ticker_df.to_excel(writer, sheet_name=ticker)
        
        # Get the xlsxwriter objects from the dataframe writer object.
        _worksheet = writer.sheets[ticker]   

        # Create a chart object.
        chart = workbook.add_chart({'type': 'line'})
        
        # Configure the series of the chart from the dataframe data.
        chart.add_series({'categories': '{t}!$A$2:$A${len}'.format(t=ticker,len=df_len),
                          'values': '={t}!$I$2:$I${len}'.format(t=ticker,len=df_len)
                          })
        chart.show_blanks_as('span')
        # Insert the chart into the worksheet.
        _worksheet.insert_chart('O2', chart)
    
        _worksheet.write('L2', 'PnL', bold)
        _worksheet.write('L3', 'Average Trade Return', bold)
        _worksheet.write('L4', 'Trades', bold)
        _worksheet.write('L5', 'Max DD', bold)
    
        _worksheet.write('M2', npnl)
        _worksheet.write('M3', avg_tret)
        _worksheet.write('M4', ttrades)
        _worksheet.write('M5', Max_Daily_Drawdown)
       
        
       
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

    

    






