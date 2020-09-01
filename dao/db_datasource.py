# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 15:13:25 2020

@author: shaileshgupta1992
"""

import dao.db_properties as ds
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import  logging
import traceback

def prod_db_conn_test():

    # Create connection
    try:
        
        host = ds.prod_db["host"]
        db = ds.prod_db["database"]
        user = ds.prod_db["user"]
        pwd = ds.prod_db["password"]
        port= ds.prod_db["port"]
        
        r_conn = psycopg2.connect(host = host, database = db, # FIXME: Use data from config file
                                  user = user, password = pwd, port = port)
        r_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
        return r_conn
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))
        
def prod_db_conn():

    # Create connection
    try:
        
        host = ds.local_db["host"]
        db = ds.local_db["database"]
        user = ds.local_db["user"]
        pwd = ds.local_db["password"]
        port= ds.local_db["port"]
        
        r_conn = psycopg2.connect(host = host, database = db, # FIXME: Use data from config file
                                  user = user, password = pwd, port = port)
        r_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
        return r_conn
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        logging.exception(str(stack_trace))