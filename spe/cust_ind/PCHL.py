import backtrader as bt
import backtrader.indicators as btind

from spe.cust_ind import pchannel

class PCHL(bt.Indicator):
    lines = ('hpchu','lpchu','hpcld','lpcld','pch','pcl','pchu_counter','pcld_counter')
    params = (
        ('period',5),
    )
    plotlines=dict(
        hpchu=dict(color='green'),
        lpchu=dict(color='green'),
        hpcld=dict(color='red'),
        lpcld=dict(color='red'),
        pch=dict(color='yellow'),
        pcl=dict(color='yellow')
    )
    def __init__(self):

        self.pchannel = pchannel.priceChannel(self.data0,period=self.p.period,subplot = False)
        self.lines.pch = self.pchannel.lines.pch
        self.l.pcl = self.pchannel.l.pcl

        self.pchu_condition = btind.crossover.CrossUp(self.data0.high,self.l.pch)
        self.pcld_condition = btind.crossover.CrossDown(self.data0.low,self.l.pcl)

        self.first = True
        self.first_pchu = True
        self.first_pcld = True

    def next(self):

        if self.first:
            self.lines.pchu_counter[0] = 0
            self.lines.pcld_counter[0] = 0
            self.first = False

        self.lines.pchu_counter[0] = self.lines.pchu_counter[-1]
        self.lines.pcld_counter[0] = self.lines.pcld_counter[-1]

        self.lines.hpchu[0] = self.lines.hpchu[-1]
        self.lines.lpchu[0] = self.lines.lpchu[-1]
        self.lines.hpcld[0] = self.lines.hpcld[-1]
        self.lines.lpcld[0] = self.lines.lpcld[-1]

        if self.pchu_condition:
            if self.first_pchu:
                self.lines.hpchu[0] = self.data0.high[0]
                self.lines.lpchu[0] = self.data0.low[0]
                self.first_pchu = False

            self.lines.pchu_counter[0] += 1
            self.lines.pcld_counter[0] = 0

        if self.pcld_condition :
            if self.first_pcld:
                self.lines.hpcld[0] = self.data0.high[0]
                self.lines.lpcld[0] = self.data0.low[0]
                self.first_pcld = False

            self.lines.pcld_counter[0] += 1
            self.lines.pchu_counter[0] = 0

        if self.lines.pchu_counter[0] == 1 and self.lines.pchu_counter[-1] == 0 :
            self.lines.hpchu[0] = self.data0.high[0]
            self.lines.lpchu[0] = self.data0.low[0]

        if self.lines.pcld_counter[0] == 1 and self.lines.pcld_counter[-1] == 0 :
            self.lines.hpcld[0] = self.data0.high[0]
            self.lines.lpcld[0] = self.data0.low[0]

