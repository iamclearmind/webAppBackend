# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:19:39 2020

@author: Harsh
"""

import spe.bt_screener as screener

def run():

    #Run Screener Module only
    all_screener_output = screener.run()
    
    return all_screener_output

if __name__ == "__main__":
    
    all_screener_output = run()