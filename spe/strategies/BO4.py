import backtrader as bt
from spe.cust_ind import pchannel
from spe.cust_ind import hhpc
class BO4(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.pricech = pchannel.priceChannel(self.data0,subplot=False)
        self.pcl = self.pricech.pcl

        self.pc50 = pchannel.priceChannel(self.data0,period=50,subplot=False)
        self.pch50 = self.pc50.pch

        self.hhpcch = hhpc.PC(self.data0,subplot=False)
        self.hhpc = self.hhpcch.hhpc

        self.order = None

        self.bar_counter = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Accepted]: #Can add order.Submitted to get that details
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Sentinel to None: new orders allowed
        # self.order = None


    def next(self):
        self.bar_counter += 1

        if self.order: # check for open orders, if so, then cancel order before issuing new.
             self.cancel(self.order)

        buyPrice = self.hhpc[0]
        if self.pch50[0] > self.hhpc[0]:
            buyPrice = self.pch50[0]

        if self.position.size < 1 and self.hhpc[0] > 0 :
            self.buy(self.data0,price=buyPrice,exectype=bt.Order.Stop)

        if self.position.size > 0 :
            self.order = self.close(self.data0,price=self.pcl[0],exectype=bt.Order.Stop)

        # To Close all open positions on last bar
        if self.position.size > 0 and len(self.data0) == (self.data.buflen() - 1):
            self.order = self.close(self.data0, size=self.params.trade_size)


    def candle_lb():
        return 1000