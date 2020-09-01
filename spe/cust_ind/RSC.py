# -*- coding: utf-8 -*-


import backtrader as bt
import backtrader.indicators as btind

class rsc(bt.Indicator):
    '''
    '''

    lines = ('rsc',)

    def __init__(self):
        
        self.l.rsc = self.data0.close/self.data1.close