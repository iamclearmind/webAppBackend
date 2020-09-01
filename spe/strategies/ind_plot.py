# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:39:41 2020

@author: harsh
"""

import backtrader as bt
from spe.cust_ind import dmi_inds

class ind_plot(bt.Strategy):

    params = (
    ('trade_size',1),
    ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        
        self.benchmark = self.getdatabyname(self.p.benchmark_name)
        
        # Initialize & assign Indicators here
        # self.rsc_channel = rscu.rscu(self.data0,self.benchmark,subplot=False)
        self.dmich = dmi_inds.DMICH(self.data0,subplot=False)
        # self.rsc_channel = rscch.RSCCH(self.data0,self.benchmark,subplot=False)
  
    def candle_lb():
        return 400