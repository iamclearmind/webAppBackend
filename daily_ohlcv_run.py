# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 18:29:27 2020

@author: Harsh
"""
import importlib
import dao.DAOModule as dao
import logging
import application_properties as ap
import os
import time
import commonUtil as cu
import traceback

def loggingFileHandlerType(fileName,fhtype):
    
    backupCount = ap.backupCount
    if fhtype == 'size':
        maxBytes = ap.max_size
        return logging.handlers.RotatingFileHandler(fileName, 
                                                maxBytes=maxBytes, backupCount=backupCount)
    elif fhtype == 'time':
        when = ap.when
        return logging.handlers.TimedRotatingFileHandler(fileName,when=when,
                                                backupCount=backupCount,utc=True)
    else:
        return logging.FileHandler(fileName)


    
def save_logs():
    
    try:
        
        datefmt = ap.datefmt
        fileNameInfo = os.path.abspath("/".join(os.getcwd().split("/", 3)[:3])) + ap.logs_folder + ap.fileName_info
        format = ap.format
        log = logging.getLogger(__name__)
        logging_type = ap.logging_type
        
        fhi = loggingFileHandlerType(fileNameInfo,logging_type)
        fhi.setLevel(logging.DEBUG)
        logging.Formatter.converter = time.gmtime
        log.addHandler(fhi)
        logging.basicConfig(level=logging.DEBUG, handlers=[fhi],
                            format=format, 
                            datefmt=datefmt)
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))

def resample_data_insert(exchange,timeframe,market_type,resample_tf) :
    
    ds_table_name = cu.get_table_name(timeframe, exchange, market_type)
    
    for r_tf in resample_tf :
        
        if r_tf <= timeframe :
            print('''Resample timeframe : {rtf} equal or less than data source timeframe : {tf}
                     Skipping {tf} to {rtf} resample'''.format(rtf=r_tf, tf = timeframe))
            continue
        
        #Generate Table names
        r_t_n_current = cu.get_table_name(r_tf, exchange, market_type)
        r_t_n_new = '''{r_t_n}_new'''.format(r_t_n=r_t_n_current)
        backup_table = '''{r_t_n}_old'''.format(r_t_n=r_t_n_current)
        
        #create table if not exsists for resampled timeframe
        dao.create_current_ohlcv_table(r_t_n_current)     # _new table is created    
        dao.resample_and_insert_data(ds_table_name, r_t_n_new,r_tf) # Insert into _new table
        
        #Rename current table to backup table
        dao.drop_table(backup_table)
        dao.rename_table(r_t_n_current,backup_table)
        
        #Rename new table to current
        dao.rename_table(r_t_n_new,r_t_n_current)


def active_exchange_ohlcv_run():
    
    #save_logs()
    datasource_list = dao.get_datasource_list()
    
    try:
        if len(datasource_list) > 0:
            for d_s in datasource_list:
                
                try:
                    
                    exchange = d_s[1]
                    timeframe = d_s[2]
                    market_type = d_s[3]
                    path = d_s[4]
                    handler = d_s[5]
                    resample_tf = d_s[6]
                            
                    module = importlib.import_module('data_handlers.'+handler)
                    ohlcv_csv_to_db_func = getattr(module, 'ohlcv_csv_to_db')
                    
                    ohlcv_csv_to_db_func(exchange, market_type, str(timeframe), path)
                    if exchange is not None and timeframe is not None and market_type is not None and resample_tf is not None:
                        
                        resample_data_insert(exchange, timeframe, market_type, resample_tf)
            
                except Exception:
                    stack_trace = traceback.format_exc()
                    print(stack_trace)
                    logging.exception(str(stack_trace))
                    continue
            return 
        else:
            print("datasource_master table can not be blank")
            logging.info("datasource_master table can not be blank") 
        
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))

if __name__ == "__main__":
    
#    if not cu.isDirectoryExist(ap.logs_folder):
#        cu.create_directory(ap.logs_folder)
    active_exchange_ohlcv_run()
