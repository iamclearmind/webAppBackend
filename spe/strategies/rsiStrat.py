# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:13:24 2020

@author: Harsh
"""
import backtrader as bt
from datetime import datetime

class rsiStrat(bt.Strategy):

    params = (
    ('benchmark_name','NSEI'),
    ('trade_size', 1),
    )
    def __init__(self):
        
        # Initialize & assign Indicators here
        self.rsi = bt.indicators.RSI_Safe(self.data.close, period=21)

    def next(self):
        
        # Conditions to be checked per candle
        if self.position.size < 100:
            if self.rsi < 40:
                self.buy(self.data,size=100)
        else:
            if self.position.size == 100 and self.rsi < 30:
                self.buy(self.data,size=100)
            # if self.position.size > 0 and self.rsi > 70:
            #     self.sell(self.data,size=100)
            if self.position.size > -100 and self.rsi > 60:
                self.sell(self.data,size=200)
                
    def strat_name():
        return 'rsiStrat'
    
    def candle_lb():
        return 21
    
