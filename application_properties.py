# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 13:31:44 2020

@author: shaileshgupta1992
"""

##### logged file configuration #######

logs_folder = "/logs"
datefmt = "%d-%m-%Y %H:%M:%S"
fileName_info = "/screener_log.log"
fileName_debug = "/screener_debug_log.log"
fileName = "/screener.log"
main_fileName = "/screener.log"
format='%(asctime)s  %(levelname)s %(message)s'

max_size = 200*1024*1024 ## 200 MB
backupCount = 3
when = "w0"
logging_type='size'

fromDate = '2000-01-01 00:00:00' 
tf_delimeter = '('
file_name_separator="#"

mark_inactive_days = 14

penny_stock_filter = { 'ns' : 10,
                      'bo' : 10,
                      'index': 0,
                      'ss' : 1,
                      'sz' : 1,
                      'f' : 1,
                      'nyse':1,
                      'nasdaq':1,
                      'amex':1,
                      }

min_tick_size = { 'bo' : 0.0005,
                 'no' : 0.0005}