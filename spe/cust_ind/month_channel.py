# -*- coding: utf-8 -*-
"""
Created on Wed Jun  17 01:00:00 2020

@author: aayush
"""

import backtrader as bt
import datetime

# Goal --> Print HH and LL of Last 5 months. Must change when month changes

class month_channel(bt.Indicator):

    lines = ('mh', 'ml', 'monthChange')
    params = (
        ('period', 5),
    )

    def __init__(self):
        self.a = 1
        self.points = []  # Stores how far behind the first bars in the last 5 months are
        self.points.append(0)
        self.first = True

    def next(self):
        if self.first:
            self.first = False
            self.l.mh[0] = 0
            self.l.ml[0] = 0
        else:
            last_month = bt.utils.num2date(self.data.datetime[-1]).date().month
            current_month = bt.utils.num2date(self.data.datetime[0]).date().month
            self.l.monthChange[0] = last_month != current_month and current_month != datetime.datetime.today().month
            self.l.mh[0] = self.l.mh[-1]
            self.l.ml[0] = self.l.ml[-1]

            if self.l.monthChange:  # If month change,
                self.points.append(0)  # add a counter 0 for the new month
                if len(self.points) > 5:
                    self.points.pop(0)  # To keep only the latest months, pop out the earliest month count
                    hi = self.data0.high.get(size=self.points[0])
                    lo = self.data0.low.get(size=self.points[0])
                    self.l.mh[0] = max(hi)  # HH of last 5 months
                    self.l.ml[0] = min(lo)  # LL of last 5 months

        # For each next(), increase the bar count by 1 for each past month in points
        self.points = [x+1 for x in self.points]
