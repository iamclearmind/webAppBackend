import backtrader as bt
import backtrader.indicators as btind
from spe.cust_ind import NEW_HIGH_STOP70
from spe.cust_ind import NEW_HIGH

class abcd(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):

        self.inds = dict()

        for d in self.datas :
            if d._name == self.p.benchmark_name :
                continue

            self.inds[d] = dict()

            self.inds[d]['newHighCH'] = NEW_HIGH.newHigh(d,subplot=False)
            self.inds[d]['newHigh'] = self.inds[d]['newHighCH'].newHigh

            self.inds[d]['newHighStop70CH'] = NEW_HIGH_STOP70.newHighstop70(d,subplot=False)
            self.inds[d]['newHighstop70'] = self.inds[d]['newHighStop70CH'].newHighstop70

            self.inds[d]['order'] = None

            self.inds[d]['hi'] = d.high
            self.inds[d]['lo'] = d.low

            self.inds[d]['eligible'] = False

            self.inds[d]['counter'] = 0

            self.inds[d]['tradeno'] = 0

        self.bar_counter = 0

        self.highest_lowest = []
        hi,lo = self.data0.high , self.data0.low

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

        for d in self.datas :

            if d._name == self.p.benchmark_name :
                continue

            # print(self.getposition(data=d).size)
            if self.inds[d]['order']: # check for open orders, if so, then cancel order before issuing new.
                self.cancel(self.inds[d]['order'])

            if self.getposition(data=d).size < self.params.trade_size  :
                self.inds[d]['order'] = self.buy(data=d,price=self.inds[d]['newHigh'][0],exectype=bt.Order.Stop)
                # print('buy condition met')

            if self.getposition(data=d).size > 0 :
                self.inds[d]['counter'] += 1
                self.inds[d]['eligible'] = True

            if self.getposition(data=d).size > 0 and d.low[0] < self.inds[d]['newHighstop70'][0]:
                self.inds[d]['order'] = self.close(data=d,price=(d.low[0] * 0.999) ,exectype=bt.Order.Stop)
                # print("sell condition met")


            if self.getposition(data=d).size == 0 and self.inds[d]['eligible'] :
                self.inds[d]['hi'] = d.high.get(size=self.inds[d]['counter'])
                self.inds[d]['lo'] = d.low.get(size=self.inds[d]['counter'])
                self.inds[d]['eligible'] = False
                # self.highest_lowest.append([self.data.num2date(),max(self.inds[d]['hi']),min(self.inds[d]['lo'])])
                self.inds[d]['tradeno'] += 1
                self.counter = 0
                print('[+] '+d.num2date().strftime("%d-%m-%Y") +' Highest in TradeNo '+ str(self.inds[d]['tradeno']) + ' of ' + str(d._name) +' is := '+ str(max(self.inds[d]['hi'])))
                print('[+] '+d.num2date().strftime("%d-%m-%Y") +' Lowest in TradeNo '+ str(self.inds[d]['tradeno']) + ' of ' + str(d._name) +' is := '+ str(min(self.inds[d]['lo'])))

    def candle_lb():
        return 1000