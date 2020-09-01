import backtrader as bt
import backtrader.indicators as btind

class PDIMDIHL(bt.Indicator):
    lines = ('hpdiu','lpdiu','hpdid','lpdid','pdi','mdi')
    plotlines=dict(
        hpdiu=dict(color='green'),
        lpdiu=dict(color='green'),
        hpdid=dict(color='red'),
        lpdid=dict(color='red'),
        pdi=dict(color='blue'),
        mdi=dict(color='yellow')
    )
    def __init__(self):
        self.l.pdi = btind.PlusDirectionalIndicator(self.data0, period=14)
        self.l.mdi = btind.MinusDirectionalIndicator(self.data0, period=14)

        self.pdiu_condition = btind.crossover.CrossUp(self.pdi(0),self.mdi(0))
        self.pdid_condition = btind.crossover.CrossDown(self.pdi(0), self.mdi(0))

        # self.plotlines.hpdiu._plotskip = True
        # self.plotlines.lpdiu._plotskip = True
        # self.plotlines.hpdid._plotskip = True
        # self.plotlines.lpdid._plotskip = True
        # self.plotlines.pdi._plotskip = True
        # self.plotlines.mdi._plotskip = True


    def next(self):

        self.l.hpdiu[0] = self.l.hpdiu[-1]
        self.l.lpdiu[0] = self.l.lpdiu[-1]
        self.l.hpdid[0] = self.l.hpdid[-1]
        self.l.lpdid[0] = self.l.lpdid[-1]

        if self.pdiu_condition:
            self.l.hpdiu[0] = self.data0.high[0]
            self.l.lpdiu[0] = self.data0.low[0]


        if self.pdid_condition :
            self.l.hpdid[0] = self.data0.high[0]
            self.l.lpdid[0] = self.data0.low[0]


