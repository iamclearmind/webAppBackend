import backtrader as bt
import backtrader.indicators as btind

from spe.cust_ind import month_channel

class MHLHL(bt.Indicator):
    lines = ('MHH','MHL','MLH','MLL','mhu_counter','mld_counter','ml','mh')
    params = (
        ('period',5),
    )
    plotlines=dict(
        MHH=dict(color='green'),
        MHL=dict(color='green'),
        MLH=dict(color='red'),
        MLL=dict(color='red'),
        mh=dict(color='blue'),
        ml=dict(color='blue'),
    )
    def __init__(self):

        self.mhl = month_channel.month_channel(self.data0,subplot = False)
        self.l.mh = self.mhl.l.mh
        self.l.ml = self.mhl.l.ml

        self.mhu_condition = btind.crossover.CrossUp(self.data0.high,self.l.mh)
        self.mld_condition = btind.crossover.CrossDown(self.data0.low,self.l.ml)

        self.first = True

    def next(self):

        self.lines.mhu_counter[0] = self.lines.mhu_counter[-1]
        self.lines.mld_counter[0] = self.lines.mld_counter[-1]

        self.lines.MHH[0] = self.lines.MHH[-1]
        self.lines.MHL[0] = self.lines.MHL[-1]
        self.lines.MLH[0] = self.lines.MLH[-1]
        self.lines.MLL[0] = self.lines.MLL[-1]

        if self.first:
            self.lines.mhu_counter[0] = 0
            self.lines.mld_counter[0] = 0
            self.first = False

        if self.mhu_condition :
            self.lines.mhu_counter[0] += 1
            self.lines.mld_counter[0] = 0

        if self.mld_condition :
            self.lines.mld_counter[0] += 1
            self.lines.mhu_counter[0] = 0

        if self.lines.mhu_counter[0] == 1 and self.lines.mhu_counter[-1] == 0 :
            self.lines.MHH[0] = self.data0.high[0]
            self.lines.MHL[0] = self.data0.low[0]

        if self.lines.mld_counter[0] == 1 and self.lines.mld_counter[-1] == 0 :
            self.lines.MLH[0] = self.data0.high[0]
            self.lines.MLL[0] = self.data0.low[0]

