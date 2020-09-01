#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015, 2016, 2017 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
#General Indicator Dependencies
from backtrader.indicators import Indicator, And, If, MovAv, ATR, crossover, SMA

# Import for DMICH
from backtrader.indicators import PlusDirectionalIndicator, MinusDirectionalIndicator, AverageDirectionalMovementIndex
# Import for BCH
from backtrader.indicators import DirectionalMovementIndex

    
class DMICH(Indicator):
    '''
    '''
    
    lines = ('range_cond','comparator', 'pdih_hhv', 'mdil_llv', 'pdih', 'mdil')
    params = ()
    plotlines = dict(top=dict(_samecolor=True), bot=dict(_samecolor=True),pdih_hhv=dict(color='green'),mdil_llv=dict(color='red'),pdih=dict(color='blue'),mdil=dict(color='blue'),)

    def __init__(self):
                    
        # Price Channels
        self.pdi = PlusDirectionalIndicator(self.data, period=14)
        self.mdi = MinusDirectionalIndicator(self.data, period=14)
        self.adx = AverageDirectionalMovementIndex(self.data, period=14)

        ## HHPC5 - LLPC5
        self.pdih_condition = crossover.CrossDown(self.pdi, self.mdi)
        self.mdil_condition = crossover.CrossUp(self.pdi, self.mdi)
        
        self.up = And(self.pdi.plusDI > self.mdi.minusDI)
        self.down = And(self.pdi.plusDI < self.mdi.minusDI)
         
        self.first_start = True
        
        # print('DMICH with data :',self.data._name)
        
        # self.plotlines.range_cond._plotskip = True
        # self.plotlines.comparator._plotskip = True
        # self.plotlines.pdih_hhv._plotskip = True
        # self.plotlines.mdil_llv._plotskip = True

    # def once(self, start, end):
    #    print('Calculation start for DMICH for Data :',self.data0._name)
       
    def next(self):
        
        #Counter Lines
        self.l.comparator[0] = self.l.comparator[-1]
        self.l.pdih_hhv[0] = self.l.pdih_hhv[-1]
        self.l.mdil_llv[0] = self.l.mdil_llv[-1]
        self.l.range_cond[0] = self.l.range_cond[-1]        
        self.l.mdil[0] = self.l.mdil[-1]
        self.l.pdih[0] = self.l.pdih[-1]
        
        if self.first_start == True :
            self.l.range_cond[0] = 0
            self.l.mdil[0] = 0
            self.l.pdih[0] = 0
            self.l.comparator[0] = 0
            self.l.pdih_hhv[0] = 0
            self.l.mdil_llv[0] = 0
            self.first_start = False
        
        if self.up[0] :
            self.l.range_cond[0] += 1
            if self.l.comparator[0] < self.data.high[0] :
                self.l.comparator[0] = self.data.high[0]
                self.l.pdih_hhv[0] = self.data.high[0]
                
        elif self.down[0]:
            self.l.range_cond[0] += 1
            if self.l.comparator[0] > self.data.low[0] :
                self.l.comparator[0] = self.data.low[0]
                self.l.mdil_llv[0] = self.data.low[0]
                
        # print('PDI :', self.pdi[0], ' | MDI :', self.mdi[0], ' | And Value :', self.up[0])
        # print(self.l.range_cond[0])
        r = int(self.l.range_cond[0])
        
        if self.pdih_condition == 1:
            self.l.pdih[0] = self.l.pdih_hhv[0]
            self.l.range_cond[0] = 0  
            # print(self.data.num2date(),':',self.l.pdih[0], 'Counter Value :' ,r)
                    
        if self.mdil_condition == 1:
            self.l.mdil[0] = self.l.mdil_llv[0]
            self.l.range_cond[0] = 0     

            
            
            
class BCH(Indicator):
    '''
    '''
    
    lines = ('range_cond','comparator', 'pgm', 'plm', 'bbh', 'rbl')
    params = (
        ('period',14),
        )
    plotlines = dict(top=dict(_samecolor=True), bot=dict(_samecolor=True),)

    def __init__(self):
                    
        # Price Channels
        self.dmi = DirectionalMovementIndex(self.data0, period=self.p.period)
        self.adx_ma = SMA(self.dmi.adx(0), period=2)
        
        # self.adx_ta = bt.talib.ADX(self.data.high,self.data.low,self.data.close,timeperiod=14)
        ## Consitions
        self.adx_cup = crossover.CrossUp(self.dmi.adx(0), self.adx_ma.sma(0))
        self.adx_cdown = crossover.CrossDown(self.dmi.adx(0), self.adx_ma.sma(0))
        
        self.counter_up = And(self.dmi.plusDI(0) > self.dmi.minusDI(0), self.dmi.adx(0) > self.adx_ma.sma(0))
        self.counter_down = And(self.dmi.plusDI(0) < self.dmi.minusDI(0), self.dmi.adx(0) > self.adx_ma.sma(0))
         
        self.pgm_cond = And(self.dmi.plusDI(0) > self.dmi.minusDI(0), self.adx_cup(0) == 1)
        self.plm_cond = And(self.dmi.plusDI(0) < self.dmi.minusDI(0), self.adx_cup(0) == 1)
        
        self.run_once = True
        self.bbh_hhv = 0
        self.rbl_llv = 0

        self.plotlines.range_cond._plotskip = True
        self.plotlines.comparator._plotskip = True
        self.plotlines.pgm._plotskip = True
        self.plotlines.plm._plotskip = True     
        
    # def once(self, start, end):
    #    print('Calculation start for BBCH for Data :',self.data0._name)
        
    def next(self):
        
        try :
            #Counter Lines
            self.l.range_cond[0] = self.l.range_cond[-1]
            self.l.comparator[0] = self.l.comparator[-1]
            self.l.pgm[0] = self.l.pgm[-1]        
            self.l.plm[0] = self.l.plm[-1]
            self.l.bbh[0] = self.l.bbh[-1]        
            self.l.rbl[0] = self.l.rbl[-1]
    
            if self.run_once == True :
                self.l.range_cond[0] = 0
                self.l.comparator[0] = 0
                self.l.pgm[0] = 0
                self.l.plm[0] = 0
                self.l.bbh[0] = 0      
                self.l.rbl[0] = 0
                self.run_once = False
                
            if self.counter_up[0] :
                self.l.range_cond[0] += 1
            elif self.counter_down[0]:
                self.l.range_cond[0] += 1
            
            r = int(self.l.range_cond[0])
            
            if self.pgm_cond[0] :
                self.l.pgm[0] = 1
            elif self.plm_cond[0] :
                self.l.plm[0] = 1
            
            if self.counter_up[0] and self.l.comparator[0] < self.data.high[0]:
                self.l.comparator[0] = self.data.high[0]
                self.bbh_hhv = self.data.high[0]
                
            if self.counter_down[0] and self.l.comparator[0] > self.data.low[0]:
                self.l.comparator[0] = self.data.low[0]
                self.rbl_llv = self.data.low[0]
                # print(f'{self.data.num2date()} | RBL Range Value : {self.l.bbh[0]} Counter Value : {r}')
                
            # print(f'{self.data.num2date()} | TALib ADX : {self.adx_ta[0]} |AXD Value : {self.dmi.adx[0]} | ADX SMA Value : {self.adx_ma.sma[0]}')
            
            
            if self.adx_cdown == 1 and self.l.plm[0] == 1:
                self.l.rbl[0] = self.rbl_llv
                self.l.range_cond[0] = 0   
                self.l.plm[0] = 0                
                # print(f'{self.data.num2date()} | RBL Value : {self.l.rbl[0]} Counter Value : {r}')
                        
            if self.adx_cdown == 1 and self.l.pgm[0] == 1:
                self.l.bbh[0] = self.bbh_hhv
                self.l.range_cond[0] = 0   
                self.l.pgm[0] = 0
                # print(f'{self.data.num2date()} | BBH Value : {self.l.bbh[0]} Counter Value : {r}')
                
            if self.adx_cdown == 1 or self.adx_cup == 1:
                self.l.range_cond[0] = 0  
    
        except ValueError as e :
            print(e)
            print('Error in Ticker :', self.data0._name)            
            