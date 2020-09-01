# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:53:42 2020

@author: harsh
"""

import backtrader as bt
from backtrader.indicators import Indicator, basicops, CrossOver, CrossUp, CrossDown
from backtrader.indicators import PlusDirectionalIndicator, MinusDirectionalIndicator

class pdicrossover(Indicator):
    lines = ('hpdiu', 'lpdiu', 'hpdid', 'lpdid', 'pdi', 'mdi')
    params = dict(
        period=14,
    )

    plotlines = dict(
        pdi=dict(color='green'),
        mdi=dict(color='red'),
        hpdiu=dict(color='blue'),
        lpdiu=dict(color='blue'),
        hpdid=dict(color='red'),
        lpdid=dict(color='red'),
    )

    def __init__(self):
        self.lines.pdi = PlusDirectionalIndicator(self.data, period=self.params.period)
        self.lines.mdi = MinusDirectionalIndicator(self.data, period=self.params.period)

        self.diu_condition = CrossUp(self.pdi(0), self.mdi(0))
        self.did_condition = CrossDown(self.pdi(0), self.mdi(0))
        self.first = True

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def next(self):
        
        if self.first:
            self.lines.hpdiu[0] = 0
            self.lines.lpdiu[0] = 0
            self.lines.hpdid[0] = 0
            self.lines.lpdid[0] = 0
            self.first = False
        else:
            self.lines.hpdiu[0] = self.lines.hpdiu[-1]
            self.lines.lpdiu[0] = self.lines.lpdiu[-1]
            self.lines.hpdid[0] = self.lines.hpdid[-1]
            self.lines.lpdid[0] = self.lines.lpdid[-1]

        if self.diu_condition[0]:
            self.lines.hpdiu[0] = self.data.high[0]
            self.lines.lpdiu[0] = self.data.low[0]
            self.log(f'Cross UP Condition Met HPDIU Val : {self.lines.hpdiu[0]}, LPDIU Val : {self.lines.lpdiu[0]}')

        if self.did_condition[0]:
            self.lines.hpdid[0] = self.data.high[0]
            self.lines.lpdid[0] = self.data.low[0]