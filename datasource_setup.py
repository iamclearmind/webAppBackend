# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 18:29:27 2020

@author: Harsh
"""
import importlib
import dao.DAOModule as dao
import logging
import traceback

def setup_datasource():
        
    try:
            
        datasource_list = dao.get_datasource_list()
    
        if len(datasource_list) > 0:
            for d_s in datasource_list:
                    
                try:
                    
                    exchange = d_s[1]
                    timeframe = str(d_s[2])
                    market_type = d_s[3]
                    path = d_s[4]
                    handler = d_s[5]
                    
                    # Build OHLCV Tables
#                    dao.create_ohlcv_table(exchange,market_type,timeframe)
                    
                    # Setup scrip_master for daily 
                    # Get func from hadler path
                    module = importlib.import_module('data_handlers.'+handler)
                    scrip_master_setup_func = getattr(module, 'scrip_master_setup')
            
                    scrip_master_setup_func(exchange,market_type,path,timeframe)
                except Exception:
                    stack_trace = traceback.format_exc()
                    print(stack_trace)
                    logging.exception(str(stack_trace))
                    continue
        else:
            print("datasource_master table can not be blank")
            logging.info("datasource_master table can not be blank")  
        
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))


if __name__ == "__main__":

    setup_datasource()
    