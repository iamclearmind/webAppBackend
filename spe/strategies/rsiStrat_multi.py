# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:13:24 2020

@author: Harsh
"""
import backtrader as bt
from datetime import datetime

class rsiStrat_multi(bt.Strategy):

    params = (
    ('benchmark_name','NSEI'),
    ('trade_size', 1),
    )

    def log(self, txt, dt=None):
        #''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
#        print('%s' % (txt))

    def __init__(self):
        
        '''
        Create an dictionary of indicators so that we can dynamically add the
        indicators to the strategy using a loop. This mean the strategy will
        work with any numner of data feeds. 
        '''
        self.trade_size = self.p.trade_perc
        
        # Initialize & assign Indicators here
        self.inds = dict()
        for i, d in enumerate(self.datas):
            if d._name == self.p.benchmark_name :
                continue
            self.log(f'Initializing Indicators for Data : {d._name}')

            self.inds[d] = dict()
            self.inds[d]['rsi'] = bt.indicators.RSI_Safe(d, period=21)

    def prenext(self):
         # Populate d_with_len
         #self.d_with_len = [d for d in self.scrips if len(d)]
         # call next() even when data is not available for all tickers
        self.next()

    def next(self):
        
        self.d_with_len = [d for d in self.datas if len(d) > 30]
        
        t_s = self.trade_size
        for i, d in enumerate(self.d_with_len):
            dt, dn = self.datetime.date(), d._name
            if d._name == self.p.benchmark_name :
                continue
            self.log(f'Next called for Data : {d._name} | {dt}')
            # Conditions to be checked per candle
            if self.getposition(d).size < t_s:
                if self.inds[d]['rsi'] < 40:
                    self.buy(d,size=t_s)
            else:
                if self.getposition(d).size == t_s and self.inds[d]['rsi'] < 30:
                    self.buy(d,size=t_s)
                # if self.position.size > 0 and self.rsi > 70:
                #     self.sell(self.data,size=100)
                if self.getposition(d).size > t_s*-1 and self.inds[d]['rsi'] > 60:
                    self.sell(d,size=t_s*2)

    def strat_name():
        return 'rsiStrat'
    
    def candle_lb():
        return 50
    
