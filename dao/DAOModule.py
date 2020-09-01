# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 13:44:46 2020

@author: shaileshgupta1992
"""
import logging
import dao.db_datasource as db
import application_properties as ap
import traceback

def close_db_connection(db_conn):
    
    try:
        
        if db_conn is not None:
            db_conn.close() # close db connection
            
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
def save_scrip_master(scrip_master_ex_list, exchange):
    
    try:
        connection = db.prod_db_conn()
        c = connection.cursor()
        records_list_template = ','.join(['%s'] * len(scrip_master_ex_list))
        
        insert_query = '''insert into scrip_master (scrip_code, company_name,
                                market_type, exchange,timeframe,file_name,isactive, created_timestamp,
                                last_updated) 
                                values {r_l_t}
                                ON CONFLICT (scrip_code,file_name)
                                DO UPDATE SET
                                market_type = excluded.market_type,
                                exchange = excluded.exchange,
                                company_name = excluded.company_name
                                '''.format(r_l_t= records_list_template)
        c.execute(insert_query, scrip_master_ex_list)
        
        # commit the transaction
        connection.commit()
        
        # close the database communication
        c.close()
        print("Records inserted successfully in :: scrip_master for exchange " + exchange)
        logging.info("Records inserted successfully in :: scrip_master for exchange " + str(exchange))
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    ## finally block Alwasy execute whether exception occured or not 
    ##  to close db connection    
    finally:
        close_db_connection(connection)

def create_temp_ohlcv_table():
    
    try:
        command =       """
                        CREATE  TEMP TABLE ohlcv_temp
                            (
                                id serial PRIMARY KEY,
                            	scrip_code character varying(20) NOT NULL,
                                interval character varying(5),
                                datetime  character varying(50),
                            	Open real,
                            	high real,
                            	low real,
                            	close real,
                            	volume real,
                                UNIQUE (scrip_code, datetime)
                            )
                            WITH (
                                OIDS = FALSE
                            )
                            TABLESPACE pg_default;
                            
                        """
                  
        return command
        
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
def create_current_ohlcv_table(d_t_n):
    
    table_name = """{tn}_new""".format(tn = d_t_n)
    
    drop_table = """DROP TABLE IF EXISTS {table}""".format(table = table_name)
                    
    command =       """
                    CREATE TABLE if not exists {table}
                        (
                            id serial PRIMARY KEY,
                        	scrip_code character varying(20) NOT NULL,
                            datetime  timestamp,
                        	Open real,
                        	high real,
                        	low real,
                        	close real,
                        	volume real,
                            UNIQUE (scrip_code, datetime)
                        )
                        WITH (
                            OIDS = FALSE
                        )
                        TABLESPACE pg_default;
                        
                    """.format(table = table_name)
                  
    try:
        r_conn = db.prod_db_conn()
        c = r_conn.cursor()   
        c.execute(drop_table)
        r_conn.commit()
        c.execute(command)
       
        # commit the transaction
        r_conn.commit()
        
        # close the database communication
        c.close()
        print(table_name + " : table created successfully")
        logging.info(table_name + " : table created successfully")
        
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    finally:
        close_db_connection(r_conn)
        
def get_scrip_list(exchange,market_type,timeframe):
    
    try:
        connection = db.prod_db_conn()
        c = connection.cursor()
        get_scrip_list_query = ''' select scrip_code, company_name,sm.file_name,
                                    dm.timeframe_m as tf,sm.id 
                                    from scrip_master sm
                                    inner join datasource_master dm on dm.exchange = sm.exchange 
                                    and dm.timeframe_m = sm.timeframe and dm.market_type = sm.market_type
                                    where dm.timeframe_m = {tf} and dm.exchange = '{ex}'
                                    	and dm.market_type = '{mt}' and sm.isactive in ('y','t')
                                    '''.format(ex=exchange, mt=market_type, tf=timeframe)

        c.execute(get_scrip_list_query)
        scrip_list = c.fetchall()  
        
        # close the database communication
        c.close()
        
        return scrip_list
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
         
    finally:
        close_db_connection(connection)
        
def get_datasource_list():
    
    try:
        
        connection = db.prod_db_conn()
        c = connection.cursor()
        get_datasource_list_query = ''' select id,exchange,timeframe_m,market_type,path,
                                        handler_path,resample_tf
                                        from datasource_master where isactive = 'y' '''
    
        c.execute(get_datasource_list_query)
        datasource_list = c.fetchall()
        
        # close the database communication
        c.close()
        
        return datasource_list
    
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    finally:
        close_db_connection(connection)
        
def create_ohlcv_table(exchange,market_type,timeframe):
    
    try:
        table_name = """ohlcv_{ex}_{mt}_{tf}""".format(ex=exchange,mt=market_type,tf=timeframe)
        
        command =       """
                        CREATE TABLE if not exists {table}
                            (
                                id serial PRIMARY KEY,
                            	scrip_code character varying(20) NOT NULL,
                                datetime  timestamp,
                            	Open real,
                            	high real,
                            	low real,
                            	close real,
                            	volume real,
                                UNIQUE (scrip_code, datetime)
                            )
                            WITH (
                                OIDS = FALSE
                            )
                            TABLESPACE pg_default;
                            
                        """.format(table = table_name)
                  
        r_conn = db.prod_db_conn()                    
        c = r_conn.cursor() 
        c.execute(command)
        
        # commit the transaction
        r_conn.commit()
        
        # close the database communication
        c.close()
        print(table_name + " : table for Exchange", exchange,"created successfully")
        logging.info(table_name + " : table for Exchange", exchange,"created successfully")

    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    finally:
        close_db_connection(r_conn)

def disable_scrip_code(timeframe,exchange,mt,tn):
    
    try:
        r_conn = db.prod_db_conn()                    
        c = r_conn.cursor() 
        c.callproc('disable_scrip_code', [ap.mark_inactive_days,timeframe,exchange,mt,tn])

    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    finally:
        close_db_connection(r_conn)

def resample_and_insert_data(from_table,to_table,resample_tf):
    
    try:
        r_conn = db.prod_db_conn()                    
        c = r_conn.cursor() 
        if check_table_exists(from_table) and resample_tf is not None and resample_tf==10080:
            print('Resampling Daily to Weekly')
            c.callproc('resample_daily_to_weekly', [from_table,to_table])
        elif check_table_exists(from_table) and resample_tf is not None and resample_tf==43200:
            print('Resampling Daily to Monthly')
            c.callproc('resample_daily_to_monthly', [from_table,to_table])
        else:
            print(from_table +": table does not exists for resampling")
            logging.info(from_table +": table does not exists for resampling")

    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    finally:
        close_db_connection(r_conn)

def save_data_error(scrip_code_id_list,error_text,exchange,function_name):
    
    try:
        data_error_tuple = [(scrip_code_id_list,error_text,exchange,function_name)]
        connection = db.prod_db_conn()
        c = connection.cursor()
        records_list_template = ','.join(['%s'] * len(data_error_tuple))
        
        insert_query = '''insert into data_error_log (scrip_code_id_list,error,exchange,functin_name)
                                values {r_l_t}
                                '''.format(r_l_t= records_list_template)
        c.execute(insert_query, data_error_tuple)
        
        # commit the transaction
        connection.commit()
        
        # close the database communication
        c.close()
        print(exchange + " Data error record inserted successfully in :: data_error_log table")
        logging.info(exchange  + " Data error record inserted successfully in :: data_error_log table")
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    ## finally block Alwasy execute whether exception occured or not 
    ##  to close db connection    
    finally:
        close_db_connection(connection)

def update_scrip_master(scrip_code_id_list):
    
    try:
        scrip_code_id_list = tuple(scrip_code_id_list)
        connection = db.prod_db_conn()
        c = connection.cursor()
#        print(scrip_code_id_list)
        update_query = '''update scrip_master 
                          set isactive ='t' 
                          where isactive ='y' and id in {id}
                          '''.format(id = scrip_code_id_list)
        c.execute(update_query)
        
        # commit the transaction
        connection.commit()
        
        # close the database communication
        c.close()
        
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    ## finally block Alwasy execute whether exception occured or not 
    ##  to close db connection    
    finally:
        close_db_connection(connection)

def rename_table(from_table,to_table):
        
    try:
        connection = db.prod_db_conn()
        c = connection.cursor()
        
        if from_table is not None and to_table is not None:
        
            rename_current_table_query = """ALTER TABLE IF EXISTS {frm_table}
                                                RENAME TO {to_table};""".format(frm_table = from_table,to_table = to_table)
                                                
            c.execute(rename_current_table_query)
            connection.commit()
            
            print("""Table rename from {f_t} to {to_t}""".format(f_t =from_table,to_t = to_table))
            logging.info("""Table rename from {f_t} to {to_t}""".format(f_t =from_table,to_t = to_table))
                                    
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    ## finally block Alwasy execute whether exception occured or not 
    ##  to close db connection    
    finally:
        close_db_connection(connection)
        
def drop_table(table_name):
        
    try:
        connection = db.prod_db_conn()
        c = connection.cursor()
        
        if table_name is not None:
        
            drop_old_table = """drop table if exists {table};""".format(table = table_name)
                
            c.execute(drop_old_table)
            connection.commit()
            
            print(table_name + " : table deleted successfully")
            logging.info(table_name + " : table deleted successfully")
                                    
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    ## finally block Alwasy execute whether exception occured or not 
    ##  to close db connection    
    finally:
        close_db_connection(connection)
        
def get_screener_list():
    
    try:
        
        connection = db.prod_db_conn()
        c = connection.cursor()
        get_screener_list_query = ''' SELECT  data_table_id, sector, screener_file, 
                                      output_colomns, csv_output_path, screener_name
                                      FROM public.screener_master sm
                                      where sm.isdeleted = 'n'
                                '''
    
        c.execute(get_screener_list_query)
        screener_list = c.fetchall()
        
        # close the database communication
        c.close()
        
        return screener_list
    
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    finally:
        close_db_connection(connection)
 
def update_empty_file_status(scrip_code_id_list):
    
    try:
        print(scrip_code_id_list)
        scrip_code_id_list = tuple(scrip_code_id_list)
        connection = db.prod_db_conn()
        c = connection.cursor()
#        print(scrip_code_id_list)
        update_query = '''update scrip_master 
                          set isactive ='e' 
                          where  id in {id}
                          '''.format(id = scrip_code_id_list)
        c.execute(update_query)
        
        # commit the transaction
        connection.commit()
        
        # close the database communication
        c.close()
        print(str(scrip_code_id_list)  + ":: Scrip code staus updated with flag e for empty file")
        logging.info(str(scrip_code_id_list)  + " ::Scrip code staus updated with flag e for empty file")
        
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
    ## finally block Alwasy execute whether exception occured or not 
    ##  to close db connection    
    finally:
        close_db_connection(connection)
		
def check_table_exists(table_name):
	 try:
			
			connection = db.prod_db_conn()
			c = connection.cursor()
			query = ''' SELECT EXISTS
						 (
						  SELECT 1 
						  FROM pg_tables
						  WHERE  tablename = '{t_n}'
						 );'''.format(t_n = table_name)
		
			c.execute(query)
			result = c.fetchone()[0]
			
			# close the database communication
			c.close()
			
			return result
		
	 except Exception:
             stack_trace = traceback.format_exc()
             print(stack_trace)
             logging.exception(str(stack_trace))
			
	 finally:
			close_db_connection(connection)
 
def insert_to_screener_value_table(data_tuple):
    
    try:
        
        connection = db.prod_db_conn()
        c = connection.cursor()
        screener_value_insert = '''   insert into screener_value_table (screener_name,date_time,data_json,last_updated)
                                        values {d_t}
                                        on conflict (screener_name, date_time)
                                        do update set
                                        data_json = excluded.data_json,
                                        last_updated = excluded.last_updated
                                '''.format(d_t=data_tuple)
    
        c.execute(screener_value_insert)
        connection.commit()
        
        # close the database communication
        c.close()

    except Exception:
            stack_trace = traceback.format_exc()
            print(stack_trace)
            logging.exception(str(stack_trace))
			
    finally:
            close_db_connection(connection)
            
def get_scrip_id_name():
    
    try:
        
        connection = db.prod_db_conn()
        c = connection.cursor()
        scrip_id_name = '''   select scrip_code, company_name from scrip_master
                                '''
        c.execute(scrip_id_name)
        scrip_id_name_list = c.fetchall()
        
        # close the database communication
        c.close()
        
    except Exception:
            stack_trace = traceback.format_exc()
            print(stack_trace)
            logging.exception(str(stack_trace))
			
    finally:
            close_db_connection(connection)
            
    return scrip_id_name_list