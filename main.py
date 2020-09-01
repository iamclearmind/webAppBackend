# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:19:39 2020

@author: Harsh
"""

#import commonUtil as cu
import spe.bt_screener as screener
import datasource_setup
import daily_ohlcv_run
import application_properties as ap
import logging
import os
import time

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
    except Exception as e:
        logging.exception(str(e))

def run():
    
    save_logs()
    #First run Data source Setup
    datasource_setup.setup_datasource()
    
    #OHLCV Ingestion Module
    daily_ohlcv_run.active_exchange_ohlcv_run()
    
    #Run Screener Module
    all_screener_output = screener.run()
    
    return all_screener_output

if __name__ == "__main__":
    
    all_screener_output = run()