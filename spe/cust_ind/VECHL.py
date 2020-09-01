import backtrader as bt
import backtrader.indicators as btind

class vechl(bt.Indicator):

    lines = ('vech','vecl')

    plotlines=dict(
        vech=dict(color='green'),
        vecl=dict(color='red')
    )

    def __init__(self):
        self.vsma = btind.SMA(self.data0.volume,period=50)

    def next(self):

        self.lines.vech[0] = self.lines.vech[-1]
        self.lines.vecl[0] = self.lines.vecl[-1]

        if (self.data0.volume[0]) > (self.vsma[0] * 5) :
            print("condition_met")
            self.lines.vech[0] = self.data0.high[0]
            self.lines.vecl[0] = self.data0.low[0]
