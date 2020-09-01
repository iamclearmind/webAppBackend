# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:11:45 2020

@author: Harsh
"""
import os
import pwd
import logging
#import math as m
import pandas as pd
import datetime
import logging.handlers
from os.path import expanduser
import application_properties as ap

import dao.DAOModule as dao

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
    
def parameters_from_data_table_id(data_table_id) :
    
    t_n_split = data_table_id.split('_')
    ex = t_n_split[1]
    m_t = t_n_split[2]
    t_f = t_n_split[3]
    
    return ex, m_t, t_f

def get_table_name(timeframe,exchange,mt):
    
    try:
        if timeframe is not None and exchange is not None and mt is not None:            
             return "ohlcv_" + exchange + "_" + mt + "_" + str(timeframe)
        return ""
    except Exception as e:
        logging.exception(str(e))
        
def strat_to_db_csv(Strat_obj,ex,m_t,t_f,screen_name):
    
    home = expanduser("~")
    url_prefix = get_server_url()
    
    scrip_id_name_list = dao.get_scrip_id_name()
    scrip_id_name_url_df = pd.DataFrame(scrip_id_name_list,columns=['sc','sn'])
    scrip_id_name_url_df['url'] = url_prefix + scrip_id_name_url_df['sc'].str.upper() + f':{ex}'.upper()
    scrip_id_name_url_df.set_index('sc',inplace=True)
    
    for k in Strat_obj:
        Strat_obj[k].update( {'Exchange' : ex.upper()} )
        # print(k,data_value_json[k])
    
    df = pd.DataFrame(Strat_obj)
    df_T = df.T
    df_T = df_T.applymap(lambda x: "{0:.6f}".format(x) if isinstance(x, (float)) else x)
    f_df = df_T.join(scrip_id_name_url_df)
    print(f_df)
    
    candle_dt = f_df['Date'].iloc[0].strftime("%d-%m-%Y") 
    now = datetime.datetime.now()
    nowiso = now.isoformat()
    df_json = f_df.to_json(orient='split',date_format='iso')
    data_tuple = (screen_name,candle_dt,df_json,nowiso)
    # dao.insert_to_screener_value_table(data_tuple)
    
    f_df.to_csv(home + '/output_data/{dt}_{s_n}_ScreenOut.csv'.format(s_n=screen_name,dt=now.strftime("%d%m%Y")))                       
    # f_df.to_csv('{dt}_{s_n}_ScreenOut.csv'.format(s_n=screen_name,dt=now.strftime("%d%m%Y")))                       

    return df_T

def get_server_url():
    username = pwd.getpwuid(os.getuid()).pw_name
    if username == 'clearmind' :
        url = 'http://192.168.1.2:9000/chart.html?t='
    elif username == 'clearmind_dev' :
        url = 'http://192.168.1.2:9010/chart.html?t='
    else :
        print('Using dev server url output link')
        url = 'http://192.168.1.2:9010/chart.html?t='
    return url