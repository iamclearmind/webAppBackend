# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:09:12 2020

@author: harsh
"""


import backtrader as bt
import backtrader.indicators as btind
from spe.cust_ind import pchannel
import datetime
        
class pcBreakout(bt.Strategy):

    params = (
    ('trade_size', 1),
    ('max_pos', 1),
    ('tick_size', 0.0005),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        
        # Initialize & assign Indicators here
        self.pc = pchannel.priceChannel(self.data,period=5,lookback=-1,subplot=False)
        
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Accepted]: #Can add order.Submitted to get that details
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Sentinel to None: new orders allowed
        self.order = None
        
    def next(self):

        if self.order: # check for open orders, if so, then cancel order before issuing new.
            self.log(f'Canceling Previous order')
            self.cancel(self.order)
            
        # Conditions to be checked per candle
        stop_entry_price = self.pc.l.pch[0] + self.p.tick_size # in next_open indicators hold last day ends value
        stop_exit_price = self.pc.l.pcl[0] - self.p.tick_size 
        
        if self.position.size == 0: # Check if pos is 0, Place buy order
            self.order = self.buy(data=self.data,size=self.params.trade_size, 
                                  price=stop_entry_price, exectype=bt.Order.Stop)
            self.log(f'Entry Order at {stop_entry_price}')
            
        elif self.position.size == self.params.trade_size: # Some position Exists, place sell order
            self.order = self.sell(data=self.data,size=self.params.trade_size,
                                   price=stop_exit_price, exectype=bt.Order.Stop)
            self.log(f'Sell Order at {stop_exit_price}')

        
    def candle_lb():
        return 1000
    