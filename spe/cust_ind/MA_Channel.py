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

from backtrader.indicators import Indicator, basicops, crossover, MovingAverage, CrossDown, CrossUp, Highest, Lowest
from backtrader.indicators import SMA

from spe.cust_ind import pchannel

class MAChannel(Indicator):

    lines = ('MACHH', 'MACHL', 'ma')
    params = dict(
        period=50,
        lookback=-1,  # consider current bar or not
    )
    plotlines=dict(
        MACHH=dict(color='green'),
        MACLL=dict(color='red')
    )

    def __init__(self):

        self.l.ma = SMA(self.data, period=self.p.period)
        self.transition = 0
        self.first_start = True
        self.highCond = CrossDown(self.data.close, self.l.ma)
        self.lowCond = CrossUp(self.data.close, self.l.ma)

        self.priceCH = pchannel.priceChannel(self.data, subplot=True)
        self.pch = self.priceCH.pch
        self.pcl = self.priceCH.pcl

    def next(self):

        if self.first_start == True:
            self.l.MACHH[0] = 0
            self.l.MACHL[0] = 0
            self.first_start = False
        else:
            self.l.MACHH[0] = self.l.MACHH[-1]
            self.l.MACHL[0] = self.l.MACHL[-1]

        if self.highCond[0]:

            hi = self.data0.high.get(size=self.transition)
            currentHI = max(hi)
            if currentHI > self.pch[0]:
                self.l.MACHH[0] = currentHI
                self.transition = 0
            else:
                self.l.MACHH[0] = self.pch[0]



        elif self.lowCond[0]:
            lo = self.data0.low.get(size=self.transition)
            currentLO = min(lo)
            if currentLO < self.pcl[0] :
                self.l.MACHL[0] = currentLO
                self.transition = 0
            else:
                self.l.MACHL[0] = self.pcl[0]

        self.transition += 1
