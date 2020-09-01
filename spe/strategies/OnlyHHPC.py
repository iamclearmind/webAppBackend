import backtrader as bt
from spe.cust_ind import hhpc
from spe.cust_ind import ayush_hhpc

class OnlyHHPC(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        #self.hhpc = hhpc.PC(self.data0, subplot=False)
        self.ahhpc = ayush_hhpc.ahhpc(self.data0,subplot=False)

    def candle_lb():
        return 1000