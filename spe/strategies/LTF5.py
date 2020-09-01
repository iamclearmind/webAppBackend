import backtrader as bt
from spe.cust_ind import rscch

class LTF5(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.benchmark = self.getdatabyname(self.p.benchmark_name)
        self.channel = rscch.RSCCH(self.data0,self.benchmark,subplot=False)
        self.rsh = self.channel.rsh
        self.rsl = self.channel.rsl

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

        if self.position.size < self.params.trade_size and self.rsh > 0:
            self.buy(self.data0, price=self.rsh[0], exectype=bt.Order.Stop)
            # print('buy condition met')

        if self.position.size > 0 :
            self.order = self.close(self.data0, price=self.rsl[0], exectype=bt.Order.Stop)
            # print("sell condition met")

    def candle_lb():
        return 0
