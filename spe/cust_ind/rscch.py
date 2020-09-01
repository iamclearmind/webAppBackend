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

from backtrader.indicators import Indicator, crossover, SMA, And

class RSCCH(Indicator):
    '''
    '''
    _mindatas = 2
    lines = ('range_cond','comparator', 'rsh', 'rsl')
    # params = ('benchmark_name','NSEI')
    plotlines = dict(top=dict(_samecolor=True), bot=dict(_samecolor=True),)

    def __init__(self):
        
        # print('Initializing RSC for Data :', self.data0._name)
        # self.benchmark = self.getdatabyname(self.p.benchmark_name)
        l_data = len(self.data0.array)
        l_bench = len(self.data1.array)
        
        if l_data != l_bench:
            raise Exception(f"Data Error in : {self.data0._name}, Please ensure data length is same for the benchmark & stock.")

        # print('Length of Stock :',l_data, 'Length of Benchmark :', l_bench)
        
        # self.data.close.get(size=1, ago=-1)
        # a = self.data1.close(-502)
        
        # Price Channels
        self.rsc = self.data0.close/self.data1.close
        self.rsc_ma = SMA(self.rsc, period=10)

        ## Up / Down cond
        self.rsc_cup = crossover.CrossUp(self.rsc, self.rsc_ma)
        self.rsc_cdown = crossover.CrossDown(self.rsc, self.rsc_ma)
        
        self.up = And(self.rsc > self.rsc_ma)
        self.down = And(self.rsc < self.rsc_ma)
         
        self.first_start = True
        self.rsh_hhv = 0
        self.rsl_llv = 0
        # print('Done Initializing RSC for Data :', self.data0._name)

        self.plotlines.range_cond._plotskip = True
        self.plotlines.comparator._plotskip = True
        # self.plotlines.rsh._plotskip = True
    # def once(self, start, end):
    #    print('Calculation start for RSCCH for Data :',self.data0._name)
        
    def next(self):
        # self.rsc = self.data0.close[0]/self.data1.close[0]
        # print('RSC val :',self.rsc[0], ' | Stock Close :', self.data0[0], ' | Benchmark Close :', self.data1[0], ' | Stock dt :',self.data0.num2date(), ' | Bench dt',self.data1.num2date() )
        try :   
            #Counter Lines
            self.l.comparator[0] = self.l.comparator[-1]
            self.l.range_cond[0] = self.l.range_cond[-1]        
            self.l.rsh[0] = self.l.rsh[-1]
            self.l.rsl[0] = self.l.rsl[-1]
            
            if self.first_start == True :
                # print('Calculation start, RSC for Data :', self.data0._name)
                self.l.range_cond[0] = 0
                self.l.comparator[0] = 0
                self.l.rsh[0] = 0
                self.l.rsl[0] = 0
                self.first_start = False
            
            if self.up[0] :
                self.l.range_cond[0] += 1
                if self.l.comparator[0] <  self.data0.high[0]:
                    self.l.comparator[0] = self.data0.high[0]
                    self.rsh_hhv = self.data0.high[0]
            elif self.down[0]:
                self.l.range_cond[0] += 1
                if self.l.comparator[0] >  self.data0.low[0]:
                    self.l.comparator[0] = self.data0.low[0]
                    self.rsl_llv = self.data0.low[0]                
                
        #     # print('PDI :', self.pdi[0], ' | MDI :', self.mdi[0], ' | And Value :', self.up[0])
            # print(self.l.range_cond[0])
            r = int(self.l.range_cond[0])
            
            if self.rsc_cup == 1:
                self.l.rsl[0] = self.rsl_llv
                self.l.range_cond[0] = 0  
                # print(self.l.rsl[0])

            if self.rsc_cdown == 1:
                self.l.rsh[0] = self.rsh_hhv
                self.l.range_cond[0] = 0     
                # print(self.l.rsh[0])
                # print(self.data.num2date(),':',self.l.rsh[0], 'Counter Value :' ,r)
        except ValueError as e :
            print(e)
            print('Error in Ticker :', self.data0._name)
            
    # def stop(self) :
    #     print('Calculation Stop, RSC for Data :', self.data0._name)