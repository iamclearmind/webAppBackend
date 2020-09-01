import backtrader as bt
from spe.cust_ind import hhpc_counter
from spe.cust_ind import hhpc

class HHPC_COUNTER_strat(bt.Strategy) :
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):

        self.hhpc = hhpc.PC(self.data0,subplot=False)

        self.hhpcCounter = hhpc_counter.counter(self.data0,subplot=False)

        self.bar_counter = 0

    def next(self):
        self.bar_counter +=1

    def candle_lb():
        return 1000