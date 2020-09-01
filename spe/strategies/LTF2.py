'''
 # @ Author: Pranav
 # @ Create Time: 2020-06-16 15:00:08
 '''


import backtrader as bt
from spe.cust_ind import hhpc
# from pymongo import MongoClient


class LTF2(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.inds = dict()

        for d in self.datas:
            if d._name == self.p.benchmark_name :
                continue

            self.inds[d] = dict()
            
            self.inds[d]['channel'] = hhpc.PC(d,subplot=False)
            self.inds[d]['hhpc'] = self.inds[d]['channel'].hhpc
            self.inds[d]['llpc'] = self.inds[d]['channel'].llpc

            self.inds[d]['order'] = None

            # self.dictionary = dict()
            self.inds[d]['dictionary'] = dict()

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

            if self.getposition(data=d).size < self.params.trade_size and self.inds[d]['hhpc'] > 0:
                self.inds[d]['order'] = self.buy(data=d, price=self.inds[d]['hhpc'][0], exectype=bt.Order.Stop)
                self.inds[d]['dictionary']['Status'] = str('BUY')
                # print('buy condition met')


            if self.getposition(data=d).size > 0 :
                self.inds[d]['order'] = self.close(data=d, price=self.inds[d]['llpc'][0], exectype=bt.Order.Stop)
                # print("sell condition met")
                self.inds[d]['dictionary']['Status'] = str('SELL')

            # To Close all open positions on last bar
            if self.getposition(data=d).size > 0 and len(d) == (d.buflen() - 1):
                self.inds[d]['order'] = self.close(data=d, size=self.params.trade_size)



        # print(self.counter)

    # def stop(self):
    #     print(self.order.status)
    #     self.dictionary['Srcipt_code'] = self.data0._name
    #
    #     if self.order.status in [self.order.Completed]:
    #
    #         if self.order.isbuy():
    #
    #         elif self.order.isclose():
    #
    #         else:
    #             self.dictionary['Status'] = str('HOLD')

        # client = MongoClient("mongodb+srv://devendra:peSyS7YTgPtYwOHI@cluster0.b3n0m.mongodb.net/data?retryWrites=true&w=majority")
        # db = client.data
        # db.data.insert_one(self.dictionary)

    def candle_lb():
        return 0


