# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 18:39:44 2018

@author: Admin
"""

import logging
#import math as m
import logging.handlers
import application_properties as ap
import shutil
import os
#import requests 
#from bs4 import BeautifulSoup 
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

def create_directory(direc_name):
    
    try:
#        dirpath = Path(direc_name)
        completePath = os.path.abspath(os.getcwd())  + direc_name
        
        if completePath is not None :
            shutil.rmtree(completePath)
            os.makedirs(completePath)
#        logging.info(dirpath,'directory created')
    except FileExistsError:
        # directory already exists
        pass
    except FileNotFoundError:
        os.makedirs(completePath)
         
def isDirectoryExist(dirPath):
    
    completePath = os.path.abspath(os.getcwd())  + dirPath
    
    if dirPath is not None and os.path.exists(completePath):    
        return True
    
    return False

def get_scripode_company_name(scrip):
    
    try:
        if scrip is not None:            
             scrip_code = scrip.split(ap.file_name_separator)[0]
             scrip_edited = scrip.split(ap.file_name_separator)[1]
             company_name = scrip_edited.split('.csv')[0]
             company_name = company_name.split(ap.tf_delimeter,maxsplit=1)[0].rstrip()
            
        return scrip_code,company_name
    except Exception:
        stack_trace = traceback.format_exc()
        print("There is something wrong with the file name.Please check the format")
        print(stack_trace)
        logging.exception(str(stack_trace))
        
def get_table_name(timeframe,exchange,mt):
    
    try:
        if timeframe is not None and exchange is not None and mt is not None:            
             return "ohlcv_" + exchange + "_" + mt + "_" + str(timeframe)
        return ""
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
    
def isDirectoryAndPathExists(path):
    
    try:
        
        if path is not None and os.path.exists(path) and os.path.isdir(path):
            return True
        
        return False
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
def isDirectoryEmpty(path):
    
    try:
        
        if isDirectoryAndPathExists(path) and len(os.listdir(path)) == 0:
            return True
        
        return False
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))

def isFileExists(file_path):
    
    try:
        if file_path is not None and os.path.exists(file_path) :
            return True
        
        return False
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))

def isEmpty(file_path):
    
    try:
        if isFileExists(file_path) and os.stat(file_path).st_size == 0:
            return True
        
        return False
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))

