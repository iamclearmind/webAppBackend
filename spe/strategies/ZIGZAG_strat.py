import backtrader as bt
from spe.cust_ind import cm_zigzag

class ZIGZAG_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):

        self.zigzag = cm_zigzag.zigzag(self.data0,subplot=False)



    def candle_lb():
        return 1000