import backtrader as bt
from spe.cust_ind import MAHL
class MAHL_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        self.channel = MAHL.MAHL(self.data0,subplot=False)


    def candle_lb():
        return 1000