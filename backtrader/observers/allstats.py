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
from .. import Observer
import math, statistics

class AllStats(Observer):

    _stclock = True
    
#    params = (
#    ('val_adj_cash', 1),
#    )
   
    lines = ('glev','exce_price','value','logr','grossr','btcr')
    
#    def start(self):
#        
#        self.lines.glev[0] = 0   
    
    def next(self):
        
        self.lines.value[0] = value = self._owner.broker.getvalue()
        self.lines.exce_price[0] = 0
        self.lines.glev[0] = 0
        
        # Update exec price when order is placed
        for order in self._owner._orderspending:
#            if order.status in [order.Completed]:
            self.lines.glev[0] = (order.executed.price) / value
            self.lines.exce_price[0] = order.executed.price
        
        # Calc Gross Lev daily  
        if self.lines.exce_price[0] == 0:
            self.lines.exce_price[0] = self.lines.exce_price[-1]
            self.lines.glev[0] = (self.lines.exce_price[0]) / value
            
        # Calc logR
        self.lines.logr[0] = logr = math.log(value/ self.lines.value[-1])
        
        # BTC - Benchmark Daily returns
        self.lines.btcr[0] = math.log(self._owner.data.close[0]/ self._owner.data.close[-1])
        
        
        #Calc Gross Returns
        if not self.lines.glev[0] == 0:
           self.lines.grossr[0] = logr / self.lines.glev[0] #* self.p.val_adj_cash
           
            
        

        