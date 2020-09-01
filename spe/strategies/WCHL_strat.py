import backtrader as bt
from spe.cust_ind import WCHL

class WCHL_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        self.channels = WCHL.WCHL(self.data0, subplot=False)

    def candle_lb():
        return 1000