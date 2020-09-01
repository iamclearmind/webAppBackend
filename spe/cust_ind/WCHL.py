import backtrader as bt
import backtrader.indicators as btind


class WCHL(bt.Indicator):
    lines = ('WCH','WCL','adx','adxma')
    params = (
        ('period',5),
    )
    plotlines=dict(
        WCH=dict(color='green'),
        WCL=dict(color='red'),
    )
    def __init__(self):
        self.l.adx = btind.AverageDirectionalMovementIndex(self.data0)
        self.l.adxma = btind.SMA(self.l.adx(0),period=2)
        self.crossup_condition = btind.crossover.CrossUp(self.l.adx(0),self.l.adxma(0))
        self.hi = []
        self.lo = []

    def next(self):

        self.l.WCH[0] = self.l.WCH[-1]
        self.l.WCL[0] = self.l.WCL[-1]

        if self.adx[0] < self.adxma[0]:
            self.hi.append(self.data0.high[0])
            self.lo.append(self.data0.low[0])

        if self.crossup_condition:
            self.l.WCH[0] = max(self.hi)
            self.l.WCL[0] = min(self.lo)
            self.hi.clear()
            self.lo.clear()