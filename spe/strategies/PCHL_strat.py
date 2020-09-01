import backtrader as bt
from spe.cust_ind import PCHL

class PCHL_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        self.channels = PCHL.PCHL(self.data0, subplot=False)

    def candle_lb():
        return 1000