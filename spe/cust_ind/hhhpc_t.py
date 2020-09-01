from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
# import backtrader.indicators as btind
import datetime

from backtrader.indicators import Indicator, basicops, crossover, Cmp, Highest, Lowest, Max
from spe.cust_ind import hhpc
from spe.cust_ind import pchannel
class hhhpcT(Indicator):
    lines = ('hhhpc', 'lllpc', 'pch', 'pcl', 'hhpc', 'llpc')  # These are displayed
    params = dict(
        period=5,
        lookback=-1,  # -1 is false. Useful for backtesting
    )
    plotlines = dict(
        hhhpc=dict(color='blue'),
        lllpc=dict(color='blue'),
        hhpc=dict(color='green'),
        llpc=dict(color='green'),
        pch=dict(color='red'),
        pcl=dict(color='red')
    )

    def __init__(self):

        hi, lo = self.data.high, self.data.low
        if self.params.lookback:
            hi. lo = hi(self.params.lookback), lo(self.params.lookback)

        # Price Channels
        self.pchannel = pchannel.priceChannel(self.data0, period=self.params.period, subplot=False)
        self.lines.pch = self.pchannel.lines.pch
        self.lines.pcl = self.pchannel.lines.pcl
        self.hhllpc = hhpc.PC(self.data0, period=5, subplot=False)
        self.lines.hhpc = self.hhllpc.lines.hhpc
        self.lines.llpc = self.hhllpc.lines.llpc

        # Conditions Low < PCL and High > PCH
        # Can you please check which condition is correct?

        # CONDITION 1 - Checks crossover with the price channel of previous bar
        # (This is how Harsh Bhaiya checks in HHPC)
        # self.hhhpc_condition = crossover.CrossDown(self.data.low, self.pcl(-1))
        # self.lllpc_condition = crossover.CrossUp(self.data.high, self.pch(-1))

        # Condition 2 - Checks crossover with the price channel of current bar
        self.hhhpc_condition = crossover.CrossDown(self.data.low, self.lines.llpc)
        self.lllpc_condition = crossover.CrossUp(self.data.high, self.lines.hhpc)



        # Checking candles where High >= HHPC, Low <= LLPC
        self.overhhpc = Cmp(self.data0.high, self.lines.hhpc)
        self.underllpc = Cmp(self.lines.llpc, self.data0.low)

        # Miscellenaous Variables
        self.start = True
        self.hstart = 0  # Start of range of HHHPC. Changes when HHHPC condition met.
        self.lstart = 0  # For LLLPC

        self.hfirst = True  # 1st time condition met for HHHPC. Different behaviour
        self.lfirst = True  # For LLLPC

        # Useless transfer variables because I can't figure out
        # how to assign "Highest" to HHHPC[0] and same for LLLPC
        self.temph = Highest(hi, period=self.params.period, subplot=False)
        self.templ = Lowest(lo, period=self.params.period, subplot=False)

    def next(self):

        ## Initialization for 1st candle
        if self.start:
            self.lines.hhhpc[0] = 0
            self.lines.lllpc[0] = 0
            self.start = False
        # Initialization for every other candle
        else:
            self.lines.hhhpc[0] = self.lines.hhhpc[-1]
            self.hstart += 1
            self.lines.lllpc[0] = self.lines.lllpc[-1]
            self.lstart += 1

        # If HHHPC Condition true (Low <= PCL)
        if self.hhhpc_condition[0] == 1:
            if self.hfirst:  # For the 1st range when no HHPC is present to filter, select the Highest Bar
                self.temph[0] = (basicops.Highest(self.data0.high, period=self.hstart, subplot=False))
                self.lines.hhhpc[0] = self.temph[0]
                self.hfirst = False

            else:  # Filter bars over HHPC and select highest else don't change
                eligible = None
                print("Should get printed times: " + str(self.hstart))
                for i in range(1, self.hstart+1):  # Loop over bars within range
                    if self.overhhpc[-i] == 1:  # Find max from bars where High >= HHPC
                        print("Candidate Highs in range: " + str(self.data0.high[-i]))
                        if eligible is None:
                            eligible = self.data0.high[-i]
                        elif self.data0.high[-i] > eligible:
                            eligible = self.data0.high[-i]
                    else:
                        print("High: " + str(self.data0.high[-i]) + " and HHPC: " + str(self.lines.hhpc[-i]) + "and overhhpc: " + str(self.overhhpc[-i]))


                if eligible is not None:
                    self.lines.hhhpc[0] = eligible
            print("Range of HHHPC is " + str(self.hstart) + " at " + str(self.data0.datetime.date(0)))
            self.hstart = 0  # Set range    diff to 0
        else:
            print("HHHPC Condition False (Low not < PCL) : Low= " + str(self.data0.low[0]) + ", PCL= " + str(self.lines.pcl[0]) + ", Cond= " + str(self.hhhpc_condition[0]) + " at " + str(self.data0.datetime.date(0)))
        # If LLLPC Condition true (High >= PCH)
        if self.lllpc_condition[0] == 1:
            if self.lfirst:  # For the 1st range when no LLPC is present to filter, select the Lowest Bar
                self.templ[0] = (basicops.Lowest(self.data0.Low, period=self.lstart, subplot=False))
                self.lines.lllpc[0] = self.templ[0]
                self.lfirst = False

            else:  # Filter bars below LLPC and select lowest else don't change
                eligible = None
                for i in range(1, self.lstart+1):  # Loop over bars within range
                    if self.underllpc[-i] == 1:  # Find min from bars where Low <= LLPC
                        if eligible is None:
                            eligible = self.data0.low[-i]
                        elif self.data0.low[-i] < eligible:
                            eligible = self.data0.low[-i]
                if eligible is not None:
                    self.lines.lllpc[0] = eligible


            self.lstart = 0

