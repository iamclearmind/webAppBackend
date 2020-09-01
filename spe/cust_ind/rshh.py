from spe.cust_ind import rscch

import backtrader as bt
import backtrader.indicators as btind


class rshh(btind.Indicator):
    lines = ('rsl', 'rsh', 'rshh', 'rsll')
    params = dict(
        period=5,
        lookback=-1,
    )
    plotlines = dict(
        rsl=dict(color='red'),
        rsh=dict(color='red'),
        rshh=dict(color='green'),
        rsll=dict(color='green')
    )

    def __init__(self):

        # Initial variables
        self.rscch = rscch.RSCCH(self.data0, self.data1, subplot=False)
        self.l.rsh = self.rscch.l.rsh
        self.l.rsl = self.rscch.l.rsl

        # Check condition for modifying the indicator
        self.rshh_condition = btind.CrossDown(self.data0.low, self.l.rsl)
        self.rsll_condition = btind.CrossUp(self.data0.high, self.l.rsh)

        # Checking candles where High >= RSH, Low <= RSL
        self.over_rsh = btind.Cmp(self.data0.high, self.l.rsh)
        self.under_rsl = btind.Cmp(self.l.rsl, self.data0.low)

        # Misc Variables
        self.start = True
        # Start of ranges. Change when condition met
        self.hstart = 0
        self.lstart = 0

        self.hfirst = True
        self.lfirst = True

    def next(self):

        if self.start:
            self.l.rshh[0] = 0
            self.l.rsll[0] = 0
            self.start = False
        else:
            self.l.rshh[0] = self.l.rshh[-1]
            self.l.rsll[0] = self.l.rsll[-1]
            self.hstart += 1
            self.lstart += 1

        # If RSHH Condition true
        if self.rshh_condition[0]:
            if self.hfirst:
                hi = btind.Highest(self.data0.high, period=self.hstart, subplot=False)
                self.l.rshh = hi
                self.hfirst = False
            else:
                eligible = None
                for i in range(1, self.hstart + 1):
                    if self.over_rsh[-i] == 1:
                        if eligible is None:
                            eligible = self.data0.high[-i]
                        elif self.data0.high[-i] > eligible:
                            eligible = self.data0.high[-i]

                if eligible is not None:
                    self.l.rshh[0] = eligible
            self.hstart = 0

        # If RSLL Condition true
        if self.rsll_condition[0]:
            if self.lfirst:
                lo = btind.Lowest(self.data0.low, period=self.lstart, subplot=False)
                self.l.rsll = lo
                self.lfirst = False
            else:
                eligible = None
                for i in range(1, self.lstart + 1):
                    if self.under_rsl[-i] == 1:
                        if eligible is None:
                            eligible = self.data0.low[-i]
                        elif self.data0.low[-i] < eligible:
                            eligible = self.data0.low[-i]

                if eligible is not None:
                    self.l.rsll[0] = eligible
            self.lstart = 0
