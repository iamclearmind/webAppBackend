# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:43:19 2020

@author: Harsh
"""

import logging
import dao.DAOModule as dao
import dao.db_datasource as db
import application_properties as ap

import pandas as pd
import backtrader as bt
import backtrader.feeds as btfeeds

import spe.screenerUtil as su

def data_feed(scrip_code,ex,m_t,t_f,cerebro,min_data):

    try:
        connection = db.prod_db_conn()
        c = connection.cursor()
        
        print(f'Fetching data for {scrip_code} scrip(s) from exhange {ex}, timeframe {t_f} & market {m_t}')
        table_name = su.get_table_name(t_f, ex, m_t)

        if scrip_code == 'all' : ## For Ticker list Handling

            try:
                p_s_f_amt = ap.penny_stock_filter[ex]
            except KeyError as e:
                print('Exchange',e,'Does not exsist in Application Properties')
                print('Ensure Penny Stock filter Exchange amount pair in Application Properties')

            # Data fetch required candles from DB by query
            c.execute('''with scrips_with_close_filter AS (select scdtc.scrip_code from (select distinct on (scrip_code) scrip_code,datetime,close
                        FROM {t_n}
                        order by scrip_code, datetime DESC) as scdtc
                        inner join scrip_master sm on scdtc.scrip_code = sm.scrip_code
                        where scdtc.close > {sf} and sm.isactive in ('t' , 'y'))
                                              
                        SELECT scrip_code, array_agg(Array[datetime::text,open::text,high::text,low::text,close::text,volume::text])
                        FROM  (SELECT n.datetime,n.open,n.high,n.low,n.close,n.volume,n.scrip_code
                        FROM {t_n} as n 
                        inner join scrips_with_close_filter cf on n.scrip_code = cf.scrip_code
                         ORDER BY n.scrip_code, n.datetime ASC) as ol

                        GROUP BY ol.scrip_code;'''.format(t_n=table_name,sf=p_s_f_amt,candles=min_data))
             
            scrip_data_list = c.fetchall()
            
            for scrip in scrip_data_list:
                try:
                    scrip_name = scrip[0]
                    print(scrip_name)
                    df = pd.DataFrame.from_records(scrip[1],columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                    df2 = df.astype({'datetime': 'datetime64[ns]', 'open': 'float64', 'high': 'float64',
                                     'low': 'float64', 'close': 'float64', 'volume': 'float64'})
                    # print(df2)
                    
                    if len(df2) < min_data:
                        print('Minimum candles not present, skipping',scrip_name)
                        continue
                        
                    # Create a Data Feed
                    data = btfeeds.PandasData(dataname=df2,
                                              timeframe=bt.TimeFrame.Days,
                                              compression=1,
                                              datetime=0,
                                              high=2,
                                              low=3,
                                              open=1,
                                              close=4,
                                              volume=5,
                                              openinterest=-1
                                                 )
                  
                    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Weeks,
                    #                         compression=1, name=scrip_name)
                        
                    cerebro.adddata(data,name=scrip_name)
                    
                except Exception as e:
                    # err.error_log(str(e),data_feed.__name__,'bt_run')
                    logging.exception(str(e))

        elif isinstance(scrip_code, tuple) :
            
            for scrip in scrip_code :
                try:
                    df = pd.read_sql_query('''Select * from (
                                            SELECT datetime,open,high,low,close,volume
                                            FROM "{t_n}" 
            								 WHERE scrip_code = '{sc}'
            								 ORDER BY datetime DESC ) as c_d
                                             order by datetime ASC
                                                 '''.format(t_n=table_name,
                                                 sc=scrip,c=min_data),con=connection)
        
                    if len(df) < min_data:
                        print('Minimum candles not present')       
                        continue
                    
                    # Create a Data Feed
                    data = btfeeds.PandasData(dataname=df,
                                              timeframe=bt.TimeFrame.Days,
                                              compression=1,
                                              datetime=0,
                                              high=2,
                                              low=3,
                                              open=1,
                                              close=4,
                                              volume=5,
                                              openinterest=-1
                                                  )
                        
                    cerebro.adddata(data,name=scrip)

                except Exception as e:
                    # err.error_log(str(e),data_feed.__name__,'bt_run')
                    logging.exception(str(e))            

        else : ## For Single Ticker Handling
            df = pd.read_sql_query('''
                                   Select * from (
                                   SELECT datetime,open,high,low,close,volume
                                         FROM "{t_n}" 
            								 WHERE scrip_code = '{sc}'
            								 ORDER BY datetime DESC ) as c_d
                                             order by datetime ASC
                                             '''.format(t_n=table_name,
                                             sc=scrip_code, c=min_data),con=connection)
            
            # print(df)
            if len(df) < min_data:
                print('Minimum candles not present')       
                return
            # Create a Data Feed
            data = btfeeds.PandasData(dataname=df,
                                      timeframe=bt.TimeFrame.Days,
                                      compression=1,
                                      datetime=0,
                                      high=2,
                                      low=3,
                                      open=1,
                                      close=4,
                                      volume=5,
                                      openinterest=-1
                                          )
                
            cerebro.adddata(data,name=scrip_code)
            
        ## Add Benchmark Data to Cerebro
            
        b_data, benchmark_name = benchmark_data(ex,m_t,t_f,min_data)
        cerebro.adddata(b_data,name=benchmark_name)
        print('Benchmark Added')
        return cerebro

    except Exception as e:
        logging.exception(str(e))
        
    finally:
        dao.close_db_connection(connection)    
    
def benchmark_data(exchange, market_type, res, data_len):
    
    try:
        connection = db.prod_db_conn()
        c = connection.cursor()    
    
        # Get name of benchmark datas for the exchange sectors
        c.execute('''select benchmark from benchmark_master 
                  where exchange = '{ex}' '''.format(ex=exchange.lower()))
        
        benchmark_id = c.fetchall()[0][0]
        
        # Data fetch required candles from DB by query
        df = pd.read_sql_query('''Select * from (
                                    select datetime,open,high,low,close,volume
                                    from ohlcv_index_{mt}_{r}
                                    where scrip_code = '{bid}'
                                    ORDER BY datetime DESC ) as c_d
                                    order by datetime ASC
                               '''.format(bid=benchmark_id,mt=market_type,r=str(res),c=data_len),con=connection)
        
         # Create a Data Feed
        data = btfeeds.PandasData(dataname=df,
                                  timeframe=bt.TimeFrame.Days,
                                  compression=1,
                                  datetime=0,
                                  high=2,
                                  low=3,
                                  open=1,
                                  close=4,
                                  volume=5,
                                  openinterest=-1
                                     )
        benchmark_name = benchmark_id.split('.')[1]
        
        return data, benchmark_name

    except Exception as e:
        logging.exception(str(e))
        
    finally:
        dao.close_db_connection(connection)
        
def benchmark_name(exchange):

    try:
        connection = db.prod_db_conn()
        c = connection.cursor()
        c.execute('''select benchmark from benchmark_master 
                  where exchange = '{ex}' '''.format(ex=exchange.lower()))
        
        benchmark_id = c.fetchall()[0][0]
        benchmark_name = benchmark_id.split('.')[1]
        
        return benchmark_name
    
    except Exception as e:
        logging.exception(str(e))
        
    finally:
        dao.close_db_connection(connection)
