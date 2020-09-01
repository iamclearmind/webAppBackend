import backtrader as bt
from spe.cust_ind import hhpc_10per
from spe.cust_ind import hhpc

class hhpc_10per_strat(bt.Strategy) :
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):

        self.hhpcch = hhpc.PC(self.data0,subplot=False)
        self.hhpc = self.hhpcch.hhpc
        self.llpc = self.hhpcch.llpc

        self.hhpc_10perCH = hhpc_10per.hhpc_10per(self.data0,subplot=False)
        self.hhpc_10per = self.hhpc_10perCH.hhpc_10per
        self.llpc_10per = self.hhpc_10perCH.llpc_10per


    def candle_lb():
        return 1000