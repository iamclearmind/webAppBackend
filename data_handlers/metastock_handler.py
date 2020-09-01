# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 16:57:59 2020

@author: Harsh
"""

import glob, os
import datetime
import psycopg2
import dao.db_datasource as db
import dao.DAOModule as dao
import logging
import fnmatch
import application_properties as ap
import commonUtil as cu
#TODO: Add logging
#TODO: Move Table SQL queries to sql folder
#TODO: Convert to class
import traceback

def get_csv_list_from_path(path):
    
    try:
         metastock_csv_list = []
         if cu.isDirectoryAndPathExists(path) :
            extension = 'csv'
            os.chdir(path)
    #        metastock_csv_list = glob.glob('*.{}'.format(extension))
            #metastock_csv_list = os.path('.').glob.glob('*.csv')
            if cu.isDirectoryEmpty(path) :
                  print(path + ":: Directory is empty")
                  logging.info(path + ":: Directory is empty")
            
            else:   
                for file in os.listdir('.'):
                    if fnmatch.fnmatch(file, '*.{}'.format(extension)):
                        metastock_csv_list.append(file)
        #        print(metastock_csv_list)
        
            return metastock_csv_list
         else:
            print(path +" :: Directory don't exists")
            logging.info(path +" :: Directory don't exists")
            
         return metastock_csv_list
            
    
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))

def scrip_master_setup(exchange, market_type, path,timeframe):
    
    scrip_master_ex_list = []
    metastock_csv_list = get_csv_list_from_path(path)
    try:
        
        if len(metastock_csv_list) > 0:
            
            for scrip in metastock_csv_list:
                
                file_name = scrip
                scrip_code,company_name = cu.get_scripode_company_name(scrip)
                
                scrip_master_row = (scrip_code, company_name, market_type, exchange,timeframe,file_name,
                                         'y', datetime.datetime.now(), datetime.datetime.now())
                
                scrip_master_ex_list.append(scrip_master_row)
            
            if len(scrip_master_ex_list) > 0:
                
                dao.save_scrip_master(scrip_master_ex_list, exchange)
        
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
    
    return 

def ohlcv_csv_to_db(exchange, market_type, timeframe, path):
    
    scrip_list = dao.get_scrip_list(exchange,market_type,timeframe) 
    
    if len(scrip_list) > 0 :
        
        if cu.isDirectoryAndPathExists(path) :
            
            if cu.isDirectoryEmpty(path) :
                print(path + ":: Directory is empty")
                logging.info(path + ":: Directory is empty")
                
            else:
                
                fromDate = ap.fromDate
                r_conn = db.prod_db_conn()
                c = r_conn.cursor()
                scrip_code_id_list = []
                empty_file_scrip_code_id = []
                error_text = ""
                dynamic_table_name = cu.get_table_name(timeframe,exchange,market_type)
                
                temp_ohlcv_query = dao.create_temp_ohlcv_table()  
                c.execute(temp_ohlcv_query) # Temp table session start
                
                logging.info("ohlcv_temp table created successfully..")
                print("ohlcv_temp table created successfully..")
                
                dao.create_current_ohlcv_table(dynamic_table_name)
                
                table_name = '{d_t_n}_new'.format(d_t_n = dynamic_table_name)
            
                insert_ohlcv_query = """insert into {t_n}(scrip_code,datetime,open,high,low,close,volume)
                                        select scrip_code,datetime::timestamp,open,high,low,close,volume
                                        from ohlcv_temp where datetime::timestamp >= '{frm_date}';
                                        """.format(t_n = table_name,frm_date = fromDate)
                
            #    print(insert_ohlcv_query)
                logging.info("Copying CSV data to ohlcv_temp table is in Progress..")
                print("Copying CSV data to ohlcv_temp table is in Progress..")
                
                for scrip_data in scrip_list:
                    
                    scrip_code_id = scrip_data[4]
            #        scrip_code = scrip_data[0]
            #        company_name = scrip_data[1]
                    file_name = scrip_data[2]
            #        scrip_csv_name = scrip_code + '#' + company_name +'.csv'
                    csv_complete_pth = path + file_name
                    
                    try: 
                        
                        if cu.isFileExists(csv_complete_pth):
                            
                            if not cu.isEmpty(csv_complete_pth):
                                
                                with open(csv_complete_pth, 'r') as f:
                        
                                    next(f) # Skip the header row.
                                    c.copy_from(f, 'ohlcv_temp', sep=',', columns=['scrip_code', 'interval', 
                                                                               'datetime', 'open', 
                                                                             'high', 'low',
                                                                               'close','volume'])
                            else:
                                empty_file_scrip_code_id.append(scrip_code_id)
                                print('File is Empty',file_name)
                                logging.info('File is Empty' + str(file_name))
                                continue
                        else:
                            scrip_code_id_list.append(scrip_code_id)
                            error_text = "File Not Found"
                            print('File not found for scrip',file_name)
                            logging.info('File not found for scrip' + str(file_name))
                            continue
                    
                    except psycopg2.IntegrityError as e :
                        stack_trace = traceback.format_exc()
                        print('Possible Duplicate Entries',file_name)
                        logging.exception(str(stack_trace))
                        print(str(e) + stack_trace)
                        continue
                    except psycopg2.DataError as e :
                        scrip_code_id_list.append(scrip_code_id)
                        error_text = "DataError"
                        print('Possible DataError',file_name)
                        logging.exception(str(e))
                        print(e)
                        continue
                    except psycopg2.Error as e :
                        stack_trace = traceback.format_exc()
                        print('General Error in',file_name)
                        logging.exception(str(stack_trace))
                        print(str(e) + stack_trace)
                        continue
                    except Exception as e:
                        stack_trace = traceback.format_exc()
                        print(str(e) + stack_trace)
                        print('General Error in111',file_name)
                        logging.exception(str(stack_trace))
                        continue
            
                try:
            
                    logging.info("Started transfering data from ohlcv_temp table to main table...")
                    print("Started transfering data from ohlcv_temp table to main table...")
                    c.execute(insert_ohlcv_query)
                    r_conn.commit()
                    
                    print("Records inserted successfully from temp_table to ::" + table_name)
                    logging.info("Records inserted successfully from temp_table to ::" + table_name)
                    
                    old_ohlv_table_name = """{d_t_n}_old""".format(d_t_n = dynamic_table_name)
                    
                    dao.drop_table(old_ohlv_table_name)
                    
                    from_table_name = dynamic_table_name
                    to_table_name = old_ohlv_table_name
                    
                    dao.rename_table(from_table_name,to_table_name)
                    
                    from_table_name = table_name
                    to_table_name = dynamic_table_name
                    
                    dao.rename_table(from_table_name,to_table_name)
                    
                    if len(scrip_code_id_list) > 0:
                        
                        dao.save_data_error(scrip_code_id_list,error_text,exchange,ohlcv_csv_to_db.__name__)
                        dao.update_scrip_master(scrip_code_id_list)
                        
                    if len(empty_file_scrip_code_id) > 0 :
                        ## update the scrip_code status to 'e' if any file is empty 
                        dao.update_empty_file_status(empty_file_scrip_code_id)
                        
                    ### update isactive='n' in scrip_code table if we did not 
                    ### receive data for any scrip_code in last 7 Days
                    
                    ### update isactive='t' in scrip_code table if we did not 
                    ### receive data for any scrip_code within 7 days (temporarily in active)
            
                    dao.disable_scrip_code(timeframe,exchange,market_type,dynamic_table_name)
                    print("scrip_code disabled successsfully..")
                        
                except Exception:
                    stack_trace = traceback.format_exc()
                    print(stack_trace)
                    logging.exception(str(stack_trace))
                    
                ## finally block Alwasy execute whether exception occured or not 
                ##  to close db connection 
                finally:
                    c.close()
                    r_conn.close() # This closes temp_table session
        else:
            print(path +" :: Directory don't exists")
            logging.info(path +" :: Directory don't exists")
    else:
         print("All scrip code is in active for exchange :" + exchange + "," + timeframe)
         logging.info("All scrip code is in active for exchange :" + str(exchange) + "," + str(timeframe))
    
    
        
