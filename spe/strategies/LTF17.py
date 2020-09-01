import backtrader as bt
from spe.cust_ind import RSC,hhpc,pchannel


class LTF17(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.benchmark = self.getdatabyname(self.p.benchmark_name)
        self.inds = dict()

        for d in self.datas:
            if d._name == self.p.benchmark_name:
                continue

            self.inds[d] = dict()

            self.inds[d]['rsc'] = RSC.rsc(d,self.benchmark)
            self.inds[d]['rscma'] = bt.ind.SMA(self.inds[d]['rsc'],period=10)

            self.inds[d]['pc'] = hhpc.PC(d,subplot=False)
            self.inds[d]['hhpc'] = self.inds[d]['pc'].l.hhpc
            self.inds[d]['pcl'] = pchannel.priceChannel(d,subplot=False).l.pcl
            self.inds[d]['adx'] = bt.ind.AverageDirectionalMovementIndex(d)
            self.inds[d]['adxma'] = bt.ind.SMA(self.inds[d]['adx'], period=2)

            self.inds[d]['order'] = None

        self.bar_counter = 0

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
            if d._name == self.p.benchmark_name:
                continue
            if self.inds[d]['order']: # check for open orders, if so, then cancel order before issuing new.
                self.cancel(self.inds[d]['order'])

            buy_cond = self.inds[d]['rsc'][0] > self.inds[d]['rscma'][0] and d.close[0] > self.inds[d]['hhpc'][0] and self.inds[d]['adx'][0] > self.inds[d]['adxma'][0]

            if buy_cond and self.getposition(data=d).size < self.p.trade_size:
                self.inds[d]['order'] = self.buy(data=d,price=d.high[0], exectype=bt.Order.Stop)

            if self.getposition(data=d).size > 0:
                self.inds[d]['order'] = self.close(data=d,price=self.inds[d]['pcl'][0], exectype=bt.Order.Stop)

            # To Close all open positions on last bar
            if self.getposition(data=d).size > 0 and len(d) == (d.buflen() - 1):
                self.inds[d]['order'] = self.close(data=d, size=self.params.trade_size)

    def candle_lb():
        return 1000