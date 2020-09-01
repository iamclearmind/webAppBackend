import backtrader as bt
from spe.cust_ind import rshh

class RSHH_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        self.benchmark = self.getdatabyname(self.p.benchmark_name)
        self.channel = rshh.rshh(self.data0,self.benchmark,subplot=False)

    def candle_lb():
        return 1000