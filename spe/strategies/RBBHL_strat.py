import backtrader as bt
from spe.cust_ind import RBBBHL

class RBBHL_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        self.channel = RBBBHL.RBBHL(self.data0,subplot=False)

    def candle_lb():
        return 1000