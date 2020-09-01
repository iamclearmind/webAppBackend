# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:58:11 2020

@author: Harsh
"""
import os
import timeit
import importlib
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import concurrent.futures
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import spe.screenerUtil as su
import spe.data_handler as dh
import dao.DAOModule as dao
################### Path hack for Debugging & Testing Only ###################
# import sys, os
# sys.path.insert(0, os.path.abspath('..'))
# import commonUtil as cu

# import application_properties as ap
# import DAOModule as dao
# import db_dataconn as db

# def loggingFileHandlerType(fileName,fhtype):
    
#     backupCount = ap.backupCount
#     if fhtype == 'size':
#         maxBytes = ap.max_size
#         return logging.handlers.RotatingFileHandler(fileName, 
#                                                 maxBytes=maxBytes, backupCount=backupCount)
#     elif fhtype == 'time':
#         when = ap.when
#         return logging.handlers.TimedRotatingFileHandler(fileName,when=when,
#                                                 backupCount=backupCount,utc=True)
#     else:
#         return logging.FileHandler(fileName)
    
def bt_run(screener_p_list):
    
    # Create a cerebro entity
    try:
        
        cerebro = bt.Cerebro()
        # cerebro.addobserver(bt.observers.BuySell)
        
        data_table_id = screener_p_list[0]
        scrip_code = screener_p_list[1]
        strategy = screener_p_list[2]
        screen_name = screener_p_list[5]
        
        ex,m_t,t_f = su.parameters_from_data_table_id(data_table_id)
        
        bench_name = dh.benchmark_name(ex)
        # Get Class from strategy Name
        module = importlib.import_module('spe.screeners.'+strategy)
        class_name = strategy
        strategy = getattr(module, class_name)
        
        # Add a strategy
        cerebro.addstrategy(strategy, benchmark_name = bench_name)
        
        # Minimum datalength
        min_data = strategy.candle_lb()
        
        # Add the Data Feed to Cerebro
        # Returns Cerebro with datafeed attached
        cerebro_w_data = dh.data_feed(scrip_code,ex,m_t,t_f,cerebro,min_data)
        
        if cerebro_w_data is None:
            print('No Data Available')
            return []
        
        # Set our desired cash start
        cerebro_w_data.broker.setcash(100000.0)     
    
        # Set the commission - 0.1% ... divide by 100 to remove the %
        cerebro_w_data.broker.setcommission(commission=0.00)
      
        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % cerebro_w_data.broker.getvalue())
    
        # Run over everything
        strategy = cerebro_w_data.run()
        Strat = strategy[0]
        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro_w_data.broker.getvalue())
        
        df = su.strat_to_db_csv(Strat.data_value_json,ex,m_t,t_f,screen_name)
        
        return df
        
    except Exception as e:
        # err.error_log(str(e),bt_run.__name__,'bt_run')
        logging.exception(str(e))
    

def main(screener_p_list):
    
    try:
        
        df = bt_run(screener_p_list)
        # print(df)
        
        return df
    except Exception as e:
        # err.error_log(str(e),main.__name__,'bt_run')
        logging.exception(str(e))

def run():
    
    try:
        
        start = timeit.default_timer()    
            
        screener_list = dao.get_screener_list()
        
        # screener_list = [
        #                 ('ohlcv_ns_equity_10080', 'all', 'CHH', None, 'output_csv/','FFM_ns'),
        # #                 ('ohlcv_bo_equity_10080', 'all', 'cmOne', None, 'output_csv/', 'cmOne_bo'),
        #             ]
    
        all_screener_output = {}


        with concurrent.futures.ProcessPoolExecutor() as executor:
            for instance,df in zip(range(len(screener_list)),executor.map(main,screener_list)):
                if df is not None:
                    try:
                        screen_name = screener_list[instance][5]
                        all_screener_output[screen_name] = df
                    except Exception as e:
                        print(e)
                        # err.error_log(str(e),run.__name__,'bt_run')
                        logging.info(str(e))
                        continue
               
        # execution_time logger
        stop = timeit.default_timer()
        execution_time = stop - start
        print("Program Executed in "+str(execution_time) )
    except Exception as e:
        # err.error_log(str(e),run.__name__,'bt_run')
        logging.exception(str(e))
        
    return all_screener_output
        
if __name__ == "__main__":
        
    all_screener_output = run()
    

    
