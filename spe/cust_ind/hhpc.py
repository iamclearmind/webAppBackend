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

from backtrader.indicators import Indicator, basicops, crossover

import datetime

class PC(Indicator):
    '''
    '''
    
    lines = ('pch_counter', 'pcl_counter', 'hhpc', 'llpc')
    params = dict(
        period=5,
        lookback=-1,  # consider current bar or not
    )
    plotlines = dict(
        pch_counter=dict(color='white'),
        pcl_counter=dict(color='white'),
        hhpc=dict(color='green'),
        llpc=dict(color='blue')
    )

    def __init__(self):
        # Mix-in & directly from object -> does not necessarily need super
        # super(EnvelopeMixIn, self).__init__()
        
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  # move backwards as needed
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        # Price Channels
        self.pch = basicops.Highest(hi,period=self.p.period,subplot=False)
        self.pcl = basicops.Lowest(lo,period=self.p.period,subplot=False)

        ## HHPC5 - LLPC5
        self.pch_condition = crossover.CrossUp(self.data.high(0), self.pch(0))
        self.pcl_condition = crossover.CrossDown(self.data.low(0), self.pcl(0))

        self.first_start = True

        self.plotlines.pch_counter._plotskip = True
        self.plotlines.pcl_counter._plotskip = True
        self.plotlines.hhpc._plotskip = True
        # self.plotlines.llpc._plotskip = True

    # def once(self, start, end):
    #    print('Calculation start for PC for Data :',self.data0._name)
        
    def next(self):
        
        # # HHPC-LLPC Counter Lines
        self.l.pch_counter[0] = self.l.pch_counter[-1]
        self.l.pcl_counter[0] = self.l.pcl_counter[-1]
        self.l.hhpc[0] = self.l.hhpc[-1]
        self.l.llpc[0] = self.l.llpc[-1]
        
        # if self.pch[0] != self.pch[-1]:
        #     print(self.data.num2date(),':',self.pch[0])
        
        if self.first_start == True :
            self.l.hhpc[0] = 0
            self.l.llpc[0] = 0
            self.l.pch_counter[0] = 0
            self.l.pcl_counter[0] = 0
            self.first_start = False
            
        ############ HHPC-LLPC #################################
        if self.pch_condition[0] == 1:
            self.l.pch_counter[0] += 1
            self.l.pcl_counter[0] = 0
            
        if self.pcl_condition[0] == 1 :
            self.l.pcl_counter[0] += 1
            self.l.pch_counter[0] = 0

        if self.l.pch_counter[0]  == 1 and self.l.pch_counter[-1] == 0:
            self.l.llpc[0] = self.pcl[0]
            # print(self.l.llpc[0])
            
        if self.l.pcl_counter[0]  == 1 and self.l.pcl_counter[-1] == 0:
            self.l.hhpc[0] = self.pch[0]
            # print(self.data.num2date(),':',self.l.hhpc[0])
        ############ HHPC-LLPC #################################
            
        # print(self.l.pch_counter[0])
        # print(self.l.pcl_counter[0])
        
        # print(self.data0.num2date(), ' | ', self.save_date)


class NEW_PC(Indicator):
    '''
    '''
    
    lines = ('pch_counter', 'pcl_counter', 'comparator', 'hhpc', 'llpc')
    params = dict(
        period=5,
        lookback=-1,  # consider current bar or not
    )
    plotlines = dict(
        pch_counter=dict(color='white'),
        pcl_counter=dict(color='white'),
        hhpc=dict(color='green'),
        llpc=dict(color='red')
    )

    def __init__(self):
        
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  # move backwards as needed
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        # Price Channels
        self.pch = basicops.Highest(hi,period=self.p.period,plotskip=True)
        self.pcl = basicops.Lowest(lo,period=self.p.period,plotskip=True)

        ## HHPC5 - LLPC5
        self.pch_condition = crossover.CrossUp(self.data.high(0), self.pch(0))
        self.pcl_condition = crossover.CrossDown(self.data.low(0), self.pcl(0))

        self.range_lowest = 0
        self.range_highest = 0

        self.first_start = True

        self.plotlines.comparator._plotskip = True
    # def once(self, start, end):
    #    print('Calculation start for PC for Data :',self.data0._name)
        
    def next(self):
        
        # # HHPC-LLPC Counter Lines
        self.l.pch_counter[0] = self.l.pch_counter[-1]
        self.l.pcl_counter[0] = self.l.pcl_counter[-1]
        self.l.comparator[0] = self.l.comparator[-1]
        self.l.hhpc[0] = self.l.hhpc[-1]
        self.l.llpc[0] = self.l.llpc[-1]
        
        # if self.pch[0] != self.pch[-1]:
        #     print(self.data.num2date(),':',self.pch[0])
        
        if self.first_start == True :
            self.l.hhpc[0] = 0
            self.l.llpc[0] = 0
            self.l.pch_counter[0] = 0
            self.l.pcl_counter[0] = 0
            self.l.comparator[0]  = 0
            self.first_start = False
            
        ############ HHPC-LLPC #################################
        
        if self.data0.low[0] < self.pcl[0]:
            if self.l.comparator[0] > self.data0.low[0]:
                self.l.comparator[0] = self.data0.low[0]
                self.range_lowest    = self.data0.low[0]
    
        if self.data0.high[0] > self.pch[0]:
            if self.l.comparator[0] < self.data0.high[0]:
                self.l.comparator[0] = self.data0.high[0]  
                self.range_highest   = self.data0.high[0] 
        
        if self.pch_condition[0] == 1:
            self.l.pch_counter[0] += 1
            self.l.pcl_counter[0] = 0
            
        if self.pcl_condition[0] == 1 :
            self.l.pcl_counter[0] += 1
            self.l.pch_counter[0] = 0

        if self.l.pch_counter[0]  == 1 and self.l.pch_counter[-1] == 0:
            self.l.llpc[0] = self.range_lowest
            # print(self.l.llpc[0])
            
        if self.l.pcl_counter[0]  == 1 and self.l.pcl_counter[-1] == 0:
            self.l.hhpc[0] = self.range_highest 
            # print(self.data.num2date(),':',self.l.hhpc[0])
        ############ HHPC-LLPC #################################
            
        # print(self.l.pch_counter[0])
        # print(self.l.pcl_counter[0])
        
        # print(self.data0.num2date(), ' | ', self.save_date)
