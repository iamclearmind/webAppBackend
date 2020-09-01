import backtrader as bt
from spe.cust_ind import MA_Channel
class MA_CH_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):

        # Initialize & assign Indicators here
        self.channel = MA_Channel.MAChannel(self.data0,subplot=False)
    def candle_lb():
        return 1000