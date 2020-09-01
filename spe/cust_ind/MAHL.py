import backtrader as bt
import backtrader.indicators as btind

class MAHL(bt.Indicator):
    lines = ('mauh','maul','madh','madl','ma')
    params = (
        ('period', 25),
    )
    plotlines=dict(
        mauh=dict(color='green'),
        maul=dict(color='green'),
        madh=dict(color='red'),
        madl=dict(color='red'),
        ma=dict(color='blue')
    )
    def __init__(self):
        self.l.ma = btind.SMA(self.data0,period=self.p.period)
        self.mau_condition = btind.crossover.CrossUp(self.data0.close,self.l.ma)
        self.mad_condition = btind.crossover.CrossDown(self.data0.close, self.l.ma)
    def next(self):
        self.l.mauh[0] = self.l.mauh[-1]
        self.l.maul[0] = self.l.maul[-1]
        self.l.madh[0] = self.l.madh[-1]
        self.l.madl[0] = self.l.madl[-1]

        if self.mau_condition :
            self.l.mauh[0] = self.data0.high[0]
            self.l.maul[0] = self.data0.low[0]

        if self.mad_condition :
            self.l.madh[0] = self.data0.high[0]
            self.l.madl[0] = self.data0.low[0]
