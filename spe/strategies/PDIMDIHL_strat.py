import backtrader as bt
import backtrader.indicators as btind
#from spe.cust_ind import pdicrossover
from spe.cust_ind import PDIMDIHL
class PDIMDIHL_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        #self.channel = pdicrossover.pdicrossover(self.data0,subplot=False)
        self.channel = PDIMDIHL.PDIMDIHL(self.data0, subplot=False)

        self.l.pdi = btind.PlusDirectionalIndicator(self.data0, period=14)
        self.l.mdi = btind.MinusDirectionalIndicator(self.data0, period=14)
    def candle_lb():
        return 1000