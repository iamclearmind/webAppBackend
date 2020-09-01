# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 11:30:09 2020

@author: harsh
"""

import backtrader as bt
import backtrader.indicators as btind

from spe.cust_ind import RSC

class rscu(bt.Indicator):
    '''
    '''

    lines = ('hrscu','lrscu','hrscd','lrscd')
    params = (
        ('rscma_period',10),
    )
    plotlines=dict(
        hrscu=dict(color='green'),
        lrscu=dict(color='green'),
        hrscd=dict(color='red'),
        lrscd=dict(color='red')
    )
    
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        
        self.rsc = RSC.rsc(self.data0,self.data1,subplot=True)
        
        self.rscma = btind.SMA(self.rsc,period=self.p.rscma_period,subplot=True)
        
        self.rsccu_cond = btind.crossover.CrossUp(self.rsc, self.rscma)
        self.rsccd_cond = btind.crossover.CrossDown(self.rsc, self.rscma)

        # self.plotlines.hrscu._plotskip = True
        self.plotlines.lrscu._plotskip = True
        self.plotlines.hrscd._plotskip = True
        # self.plotlines.lrscd._plotskip = True
        
    def next(self):
        
        self.lines.hrscu[0] = self.lines.hrscu[-1]
        self.lines.lrscu[0] = self.lines.lrscu[-1]
        self.lines.hrscd[0] = self.lines.hrscd[-1]
        self.lines.lrscd[0] = self.lines.lrscd[-1]        
        
        if self.rsccu_cond :
            # self.log(f'Cross Up condition met, High Value {self.data0.high[0]}')
            self.lines.hrscu[0] = self.data0.high[0]
            self.lines.lrscu[0] = self.data0.low[0]  
            
        if self.rsccd_cond :
            # self.log(f'Cross Down condition met, High Value {self.data0.high[0]}')
            self.lines.hrscd[0] = self.data0.high[0]
            self.lines.lrscd[0] = self.data0.low[0]           
            

        