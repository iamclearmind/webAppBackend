import backtrader as bt
import backtrader.indicators as btind

class RBBHL(bt.Indicator):
    lines = ('hbb','lbb','hrb','lrb','pdi','mdi','adx','adxma')

    plotlines=dict(
        hbb=dict(color='green'),
        lbr=dict(color='blue'),
        hrb=dict(color='red'),
        lrb=dict(color='red'),
        pdi=dict(color='blue'),
        mdi=dict(color='yellow'),
        adx=dict(color='green'),
        adxma=dict(color='red')
    )
    def __init__(self):
        self.l.pdi = btind.PlusDirectionalIndicator(self.data0, period=14)
        self.l.mdi = btind.MinusDirectionalIndicator(self.data0, period=14)
        self.l.adx = btind.AverageDirectionalMovementIndex(self.data0,period=14)
        self.l.adxma = btind.SMA(self.l.adx,period=2)
        self.adx_condition = btind.crossover.CrossUp(self.adx(0),self.adxma(0))

        # self.plotlines.lbb._plotskip = True
        # self.plotlines.hrb._plotskip = True
        # self.plotlines.lrb._plotskip = True
        # self.plotlines.pdi._plotskip = True
        # self.plotlines.mdi._plotskip = True
        # self.plotlines.adx._plotskip = True
        # self.plotlines.adxma._plotskip = True


    def next(self):

        self.l.hbb[0] = self.l.hbb[-1]
        self.l.lbb[0] = self.l.lbb[-1]
        self.l.hrb[0] = self.l.hrb[-1]
        self.l.lrb[0] = self.l.lrb[-1]

        if self.l.pdi[0] > self.l.mdi[0] and self.adx_condition:
            self.l.hbb[0] = self.data0.high[0]
            self.l.lbb[0] = self.data0.low[0]


        if self.l.pdi[0] < self.l.mdi[0] and self.adx_condition :
            self.l.hrb[0] = self.data0.high[0]
            self.l.lrb[0] = self.data0.low[0]

