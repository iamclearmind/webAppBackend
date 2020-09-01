import backtrader as bt
from spe.cust_ind import month_channel
class Monu_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):

        # Initialize & assign Indicators here
        self.channel = month_channel.month_channel(self.data0,subplot=False)
    def candle_lb():
        return 1000