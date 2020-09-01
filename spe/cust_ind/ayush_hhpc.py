# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 11:20:21 2020

@author: harsh
"""


import backtrader as bt
import backtrader.indicators as btind

from spe.cust_ind import pchannel

class ahhpc(bt.Indicator):
    '''
    '''

    lines = ('hhpc','llpc')
    # params = (
    #     ('period',5),
    # )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), str(txt)))

    def __init__(self):
        
        self.pricechannel = pchannel.priceChannel(self.data,period=5,subplot=True)
        
        self.pch = self.pricechannel.pch
        self.pcl = self.pricechannel.pcl
    
        self.hhpcCurrent = 0.0
        self.llpcCurrent = 0.0
        self.highDone = False
        self.first = True
        
    def next(self):

        self.l.hhpc[0] = self.l.hhpc[-1]
        self.l.llpc[0] = self.l.llpc[-1]
        
        # print('PCH Value',self.pch[0])
        # print('PCL Value',self.pcl[0])
        
        if (self.first or not self.highDone) and self.data0.low[0] < self.pcl[0]:
            self.hhpcCurrent = self.pch[0]
            self.highDone = True
            self.first = False
            self.l.hhpc[0] = self.pch[0]
            self.log(f'HHPC Condition met, hhpc value: {self.pch[0]}')
            
        elif (self.first or self.highDone) and self.data0.high[0] > self.pch[0]:
            self.llpcCurrent = self.pcl[0]
            self.highDone = False
            self.first = False
            self.l.llpc[0] = self.pcl[0]
            self.log(f'LLPC Condition met, llpc value: {self.pcl[0]}')        
        
        else :
            self.l.hhpc[0] = self.l.hhpc[-1]
            self.l.llpc[0] =  self.l.llpc[-1]
            

        
       