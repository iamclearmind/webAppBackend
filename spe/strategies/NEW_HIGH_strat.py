import backtrader as bt
from spe.cust_ind import NEW_HIGH
from spe.cust_ind import NEW_HIGH_STOP70
from spe.cust_ind import NEW_HIGH_STOP75
from spe.cust_ind import NEW_HIGH_STOP50
from spe.cust_ind import NEW_HIGH_STOP80
from spe.cust_ind import NEW_HIGH_STOP85
from spe.cust_ind import NEW_HIGH_STOP90


class NEW_HIGH_strat(bt.Strategy) :
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
    )

    def __init__(self):
        self.newHighch = NEW_HIGH.newHigh(self.data0,subplot=False)
        self.newHigh = self.newHighch.newHigh

        self.newHighstop70ch = NEW_HIGH_STOP70.newHighstop70(self.data0,subplot=False)
        self.newHighstop70 = self.newHighstop70ch.newHighstop70

        self.newHighstop75ch = NEW_HIGH_STOP75.newHighstop75(self.data0, subplot=False)
        self.newHighstop75 = self.newHighstop75ch.newHighstop75

        self.newHighstop50ch = NEW_HIGH_STOP50.newHighstop50(self.data0, subplot=False)
        self.newHighstop50 = self.newHighstop50ch.newHighstop50

        self.newHighstop80ch = NEW_HIGH_STOP80.newHighstop80(self.data0, subplot=False)
        self.newHighstop80 = self.newHighstop80ch.newHighstop80

        self.newHighstop85ch = NEW_HIGH_STOP85.newHighstop85(self.data0, subplot=False)
        self.newHighstop85 = self.newHighstop85ch.newHighstop85

        self.newHighstop90ch = NEW_HIGH_STOP90.newHighstop90(self.data0, subplot=False)
        self.newHighstop90 = self.newHighstop90ch.newHighstop90

    def next(self):
        print(self.data0.num2date())
        print('current ' + str(self.newHigh[0]))
        print('previous ' + str(self.newHigh[-1]))

    def candle_lb():
        return 50