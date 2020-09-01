import backtrader as bt
from spe.cust_ind import RANGE


class RANGE_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):

        self.range = RANGE.RANGE(self.data0, subplot=True)

    def candle_lb():
        return 1000