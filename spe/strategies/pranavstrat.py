import backtrader as bt
from spe.cust_ind import rscu
from spe.cust_ind import RSC
import backtrader.indicators as btind
class pranavstrat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        self.benchmark = self.getdatabyname(self.p.benchmark_name)

        # Initialize & assign Indicators here
        self.rsc = RSC.rsc(self.data0, self.benchmark, subplot=True)
        self.rscma = btind.SMA(self.rsc,period=10,subplot=False)
        self.rsc_up = rscu.rscu(self.data0,self.benchmark,subplot=False)

    def candle_lb():
        return 1000