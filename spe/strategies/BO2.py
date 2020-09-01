import backtrader as bt
import backtrader.indicators as btind
from spe.cust_ind import dmi_inds
from spe.cust_ind import RBBBHL


class BO2(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.inds = dict()

        for d in self.datas:
            if d._name == self.p.benchmark_name:
                continue
            self.inds[d] = dict()

            self.inds[d]['csma200'] = btind.SMA(d.close, period=200)
            self.inds[d]['dmi'] = dmi_inds.BCH(d,subplot=False)
            self.inds[d]['bbh'] = self.inds[d]['dmi'].bbh
            self.inds[d]['adx'] = btind.AverageDirectionalMovementIndex(d,period=14,subplot=False)
            self.inds[d]['adxma'] = btind.SMA(self.inds[d]['adx'],period=2)

            self.inds[d]['rbbhl'] = RBBBHL.RBBHL(d,subplot=False)
            self.inds[d]['hbb'] = self.inds[d]['rbbhl'].hbb

            self.inds[d]['order'] = None
            self.inds[d]['sellStop'] = None
            self.inds[d]['onceTrue'] = False
            self.inds[d]['sell_condition'] = btind.crossover.CrossDown(self.inds[d]['adx'], self.inds[d]['adxma'])

            self.inds[d]['bar_counter'] = 0

    # def log(self, txt, dt=None):
    #     ''' Logging function fot this strategy'''
    #     dt = dt or self.data.datetime[0]
    #     if isinstance(dt, float):
    #         dt = bt.num2date(dt)
    #     print('%s, %s' % (dt.isoformat(), txt))
    #
    # def notify_order(self, order):
    #     if order.status in [order.Accepted]: #Can add order.Submitted to get that details
    #         # Buy/Sell order submitted/accepted to/by broker - Nothing to do
    #         self.log('ORDER ACCEPTED', dt=order.created.dt)
    #         self.order = order
    #         return
    #
    #     if order.status in [order.Expired]:
    #         self.log('BUY EXPIRED')
    #
    #     elif order.status in [order.Completed]:
    #         if order.isbuy():
    #             self.log(
    #                 'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
    #                 (order.executed.price,
    #                  order.executed.value,
    #                  order.executed.comm))
    #
    #         else:  # Sell
    #             self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
    #                      (order.executed.price,
    #                       order.executed.value,
    #                       order.executed.comm))
    #
    #     # Sentinel to None: new orders allowed
    #     # self.order = None

    def prenext(self):
        # Populate d_with_len
        self.d_with_len = [d for d in self.datas if len(d) > 5]
        # call next() even when data is not available for all tickers
        self.next()

    def nextstart(self):
        # This is called exactly ONCE when all datas are loaded, when next is
        # 1st called and defaults to call `next`
        self.d_with_len = self.datas  # all data sets fulfill the guarantees now

        self.next()  # delegate the work to next

    def next(self):
        for d in self.datas:
            if d._name == self.p.benchmark_name:
                continue

            self.inds[d]['bar_counter'] += 1

            if self.inds[d]['order']: # check for open orders, if so, then cancel order before issuing new.
                self.cancel(self.inds[d]['order'])

            if self.getposition(data=d).size < self.params.trade_size and d.close[0] > self.inds[d]['csma200'][0] and d.close[0] > self.inds[d]['bbh'][0]:
                self.buy(d,price=(self.inds[d]['hbb'][0] * 1.001), exectype=bt.Order.Stop)
                # print('buy condition met')

            if self.inds[d]['sell_condition']:
                self.inds[d]['sellStop'] = d.low[0] * 0.9990
                self.inds[d]['onceTrue'] = True

            if self.getposition(data=d).size > 0 and self.inds[d]['onceTrue']:
                self.inds[d]['order'] = self.close(d,price=self.inds[d]['sellStop'], exectype=bt.Order.Stop)
                # print("sell condition met")

            # To Close all open positions on last bar
            if self.getposition(data=d).size > 0 and len(d) == (d.buflen() - 1):
                self.inds[d]['order'] = self.close(d, size=self.params.trade_size)


    def candle_lb():
        return 1000