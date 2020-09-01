import backtrader as bt
from spe.cust_ind import NEW_HIGH


class newHighstop70(bt.Indicator):

    lines = ('newHighstop70',)

    plotlines=dict(
        newHigh=dict(color='green'),
    )

    def __init__(self):
        self.newHighch = NEW_HIGH.newHigh(self.data0)
        self.newHigh = self.newHighch.newHigh

    def next(self):

        self.lines.newHighstop70[0] = self.newHigh[0] * 0.7