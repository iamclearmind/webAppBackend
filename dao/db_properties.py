# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 13:38:06 2020

@author: shaileshgupta1992
"""

import os
import pwd

def get_db_name():
    username = pwd.getpwuid(os.getuid()).pw_name
    if username == 'clearmind' :
        db_name = 'cm'
    elif username == 'clearmind_dev' :
        db_name = 'cm_dev'
    else :
        raise Exception('Switch User to clearmind / clearmind_dev & Rerun the file')
    return db_name
    
######## local DB Connection ######

local_db = {
                'host' : "localhost",
                'user' : 'postgres',
                'password' : 'root$456',
                'database' : 'cm_dev',
                'port': 5432
            }
