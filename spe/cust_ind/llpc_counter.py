import backtrader as bt
from spe.cust_ind import hhpc


class counter(bt.Indicator):
    lines = ('llpc_counter',)

    def __init__(self):
        self.HHPC = hhpc.PC(self.data0,subplot=False)


    def next(self):
        self.l.llpc_counter[0] = self.l.llpc_counter[-1]
        if self.data0.close[0] <  self.HHPC.l.llpc[0]:
            self.l.llpc_counter[0] += 1

        if self.data0.close[0] > self.HHPC.l.llpc[0]:
            self.l.llpc_counter[0] = 0