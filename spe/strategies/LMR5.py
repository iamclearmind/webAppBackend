import backtrader as bt
from spe.cust_ind import RSC
import backtrader.indicators as btind
from spe.cust_ind import pchannel


class LMR5(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.benchmark = self.getdatabyname(self.p.benchmark_name)
        self.inds = dict()
        for d in self.datas :
            if d._name == self.p.benchmark_name :
                continue

            self.inds[d] = dict()

            self.inds[d]['rsc_ind'] = RSC.rsc(d,self.benchmark,subplot =False)
            self.inds[d]['rsc'] = self.inds[d]['rsc_ind'].rsc
            self.inds[d]['rscma'] = btind.SMA(self.inds[d]['rsc'],period=10,subplot=False)

            self.inds[d]['priceCH'] = pchannel.priceChannel(d,subplot=False)
            self.inds[d]['pcl'] = self.inds[d]['priceCH'].l.pcl

            self.inds[d]['order'] = None

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

    def prenext(self):
        # Populate d_with_len
        self.d_with_len = [d for d in self.datas if len(d) > 5]
        # call next() even when data is not available for all tickers
        self.next()

    def nextstart(self):
        # This is called exactly ONCE when all datas are loaded, when next is
        # 1st called and defaults to call `next`
        self.d_with_len = self.datas # all data sets fulfill the guarantees now

        self.next()  # delegate the work to next


    def next(self):

        self.bar_counter += 1

        for d in self.d_with_len:

            if d._name == self.p.benchmark_name :
                continue

            if self.inds[d]['order']: # check for open orders, if so, then cancel order before issuing new.
                self.cancel(self.inds[d]['order'])

            if self.getposition(data=d).size < self.params.trade_size and self.inds[d]['rsc'][0] > self.inds[d]['rscma'][0] and d.low[0] < self.inds[d]['pcl'][0]:
                self.inds[d]['order'] = self.buy(data=d,price=d.high[0] * 1.001, exectype=bt.Order.Stop)
                # print('buy condition met')

            # if self.getposition(data=d).size > 0 :
            #     self.inds[d]['counter'] += 1
            #     self.inds[d]['eligible'] = True

            if self.getposition(data=d).size > 0 and self.inds[d]['rsc'][0] < self.inds[d]['rsc'][-1] :
                self.inds[d]['order'] = self.close(data=d,price=d.low[0] * 0.9999, exectype=bt.Order.Stop)
                # print("sell condition met")

            # To Close all open positions on last bar
            if self.getposition(data=d).size > 0 and len(d) == (d.buflen() - 1):
                self.inds[d]['order'] = self.close(data=d, size=self.params.trade_size)


            # if self.getposition(data=d).size == 0 and self.inds[d]['eligible'] :
            #     hi = d.high.get(size=self.inds[d]['counter'])
            #     lo = d.low.get(size=self.inds[d]['counter'])
            #     self.inds[d]['eligible'] = False
            #     self.highest_lowest.append([d.num2date(),max(hi),min(lo)])
            #     print(d.num2date().strftime("%d-%m-%Y"))
            #     self.inds[d]['tradeNo'] += 1
            #     self.inds[d]['counter'] = 0
            #     print('[+] Highest in TradeNo '+ str(self.inds[d]['tradeNo']) +' is := '+ str(max(hi)))
            #     print('[+] Lowest in TradeNo '+ str(self.inds[d]['tradeNo']) +' is := '+ str(min(lo)))

    def candle_lb():
        return 1000