import backtrader as bt
from spe.cust_ind import hhpc


class hhpc_10per(bt.Indicator):

    lines = ('hhpc_10per','llpc_10per')

    plotlines=dict(
        newHigh=dict(color='green'),
    )

    def __init__(self):
        self.hhpcch = hhpc.PC(self.data0)
        self.hhpc = self.hhpcch.hhpc
        self.llpc = self.hhpcch.llpc

    def next(self):

        self.l.hhpc_10per[0] = self.hhpc[0] * 1.1
        self.l.llpc_10per[0] = self.llpc[0] * 0.9

