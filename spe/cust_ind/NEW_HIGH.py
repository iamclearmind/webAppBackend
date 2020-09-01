import backtrader as bt


class newHigh(bt.Indicator):

    lines = ('newHigh',)

    plotlines=dict(
        newHigh=dict(color='green'),
    )

    def __init__(self):
        self.first = True

    def next(self):

        self.l.newHigh[0] = self.l.newHigh[-1]

        if self.first :
            self.l.newHigh[0] = self.data0.high[0]
            self.first = False

        if self.data0.high[0] > self.l.newHigh[0] :
            self.l.newHigh[0] = self.data0.high[0]

