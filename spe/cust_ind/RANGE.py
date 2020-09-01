import backtrader as bt



class RANGE(bt.Indicator):
    lines = ('range',)

    def next(self):

        self.l.range[0] = ((self.data0.high[0] - self.data0.low[0])/self.data0.low[0]) * 100
