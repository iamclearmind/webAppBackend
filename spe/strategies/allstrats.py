# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 11:25:32 2020

@author: harsh
"""


import backtrader as bt

from spe.cust_ind import rscu
from spe.cust_ind import hhpc
from spe.cust_ind import dmi_inds
from spe.cust_ind import rscch
from spe.cust_ind import RSC

class allstrats(bt.Strategy):

    params = (
    ('trade_size',1),
    ('benchmark_name', 'NSEI'),
    ('tick_size', 0.0005),
    )

    def __init__(self):
        
        self.benchmark = self.getdatabyname(self.p.benchmark_name)
        
        # Initialize & assign Indicators here
        self.rscupdown = rscu.rscu(self.data0,self.benchmark,subplot=False)
        self.rscch = rscch.RSCCH(self.data0,self.benchmark,subplot=False)
        
        self.price_channels = hhpc.PC(self.data0,subplot=False)
        
        self.bch = dmi_inds.BCH(self.data0,period=14,subplot=False)
        self.dmich = dmi_inds.DMICH(self.data0,subplot=False)
        
        self.pdih = self.dmich.pdih
        self.mdil = self.dmich.mdil

        self.bbh = self.bch.bbh
        self.rbl = self.bch.rbl
        
        self.hhpc = self.price_channels.hhpc
        self.llpc = self.price_channels.llpc
        
        self.rschc = self.rscch.rsh
        self.rsclc = self.rscch.rsl
        
        self.hrscu = self.rscupdown.hrscu
        self.lrscu = self.rscupdown.lrscu
        self.hrscd = self.rscupdown.hrscd
        self.lrscd = self.rscupdown.lrscd        
        
        self.rsl_last_entry = None
        self.order = None
        
    def next(self):
        
        if self.order: # check for open orders, if so, then cancel order before issuing new.
            self.cancel(self.order)

        buy_cond = self.rsclc[0] > self.rsclc[-1]
        
        if self.rsl_last_entry:
            exit_price = self.rsl_last_entry * 0.99
        
        if self.position.size < self.params.trade_size * 6 and buy_cond :
            self.buy(self.data0,size=self.params.trade_size)
            self.rsl_last_entry = self.rsclc[0]
            
        if self.position.size > 0:
            self.order = self.close(self.data0,price=exit_price, exectype=bt.Order.Stop)
            

        # # Conditions to be checked per candle
        # stop_entry_price = self.rschc[0] + self.p.tick_size
        # stop_exit_price = self.rsclc[0] - self.p.tick_size 
        
        # if self.position.size == 0: # Check if pos is 0, Place buy order
        #     self.order = self.buy(data=self.data0,size=self.params.trade_size, 
        #                           price=stop_entry_price, exectype=bt.Order.Stop)
            
        # elif self.position.size == self.params.trade_size: # Some position Exists, place sell order
        #     self.order = self.sell(data=self.data0,size=self.params.trade_size,
        #                            price=stop_exit_price, exectype=bt.Order.Stop)


    def candle_lb():
        return 1000