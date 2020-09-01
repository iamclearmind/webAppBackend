# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:09:12 2020

@author: harsh
"""


import backtrader as bt
from spe.cust_ind import pchannel
        
class pcBreakout_min(bt.Strategy):

    params = (
    ('trade_size', 1),
    ('max_pos', 1),
    ('tick_size', 0.0005),
    )

    def __init__(self):
        
        # Initialize & assign Indicators here
        self.pc = pchannel.priceChannel(self.data,period=5,lookback=-1,subplot=False)
        
        self.order = None
       
    def next(self):

        if self.order: # check for open orders, if so, then cancel order before issuing new.
            self.cancel(self.order)

        # Conditions to be checked per candle
        stop_entry_price = self.pc.l.pch[0] + self.p.tick_size
        stop_exit_price = self.pc.l.pcl[0] - self.p.tick_size 
        
        if self.position.size == 0: # Check if pos is 0, Place buy order
            self.order = self.buy(data=self.data,size=self.params.trade_size, 
                                  price=stop_entry_price, exectype=bt.Order.Stop)
            
        elif self.position.size == self.params.trade_size: # Some position Exists, place sell order
            self.order = self.sell(data=self.data,size=self.params.trade_size,
                                   price=stop_exit_price, exectype=bt.Order.Stop)
            
    def candle_lb():
        return 1000
