# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 16:15:16 2020

@author: harsh
"""
import backtrader as bt
import backtrader.indicators as btind

class priceChannel(bt.Indicator):
    '''
    '''

    lines = ('pch','pcl')
    params = (
        ('period',5),
        ('lookback',-1),
    )

    def __init__(self):
        
        hi, lo = self.data.high(-1), self.data.low(-1)
            
        # Price Channels
        self.l.pch = btind.basicops.Highest(hi,period=self.p.period,subplot=False)
        self.l.pcl = btind.basicops.Lowest(lo,period=self.p.period,subplot=False)

        self.plotlines.pch._plotskip = True
        # self.plotlines.pcl._plotskip = True
